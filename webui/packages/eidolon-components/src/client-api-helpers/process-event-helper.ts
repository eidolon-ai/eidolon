import {DisplayElement, ElementsAndLookup, makeElement, MarkdownElement} from "../lib/display-elements.js";
import {createParser, ParsedEvent, ParseEvent} from "eventsource-parser";
import {ChatEvent} from "@repo/eidolon-client/client";

const processEvent = (event: ChatEvent, elements: ElementsAndLookup) => {
  const element = makeElement(event)
  if (element) {
    let lastElement: DisplayElement | undefined
    if (event.stream_context) {
      const parent = elements.lookup[event.stream_context]!
      lastElement = parent.children[parent.children.length - 1]
    } else {
      lastElement = elements.elements[elements.elements.length - 1]
    }
    if (lastElement?.type === "markdown" && element.type === "markdown") {
      const mdElement = lastElement as MarkdownElement
      mdElement.content = mdElement.content + event.content
    } else {
      if (element.type === "tool-call") {
        elements.lookup[element.contextId] = element
      } else if (element.type === "tool-call-end") {
        elements.lookup[element.contextId]!.is_active = false
      }
      if (event.stream_context) {
        const parent = elements.lookup[event.stream_context]!
        parent.children.push(element)
      } else {
        elements.elements.push(element)
      }
    }
  }
}

export async function executeServerOperation(machineUrl: string, agent: string, operation: string, processId: string,
                                             data: Record<string, any>, elementsAndLookup: ElementsAndLookup,
                                             updateElements: (elements: ElementsAndLookup) => void, cancelFetchController: AbortController) {

  const response = await fetch(`/eidolon/api/process/${processId}/messages`, {
    signal: cancelFetchController.signal,
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Accept": "text/event-stream"
    },
    body: JSON.stringify({machineUrl, agent, operation, data: data}),
  })

  const reader = response.body!.getReader();
  const decoder = new TextDecoder();

  const processChunk = (chunk: string) => {
    try {
      const eventSourceParser = createParser((inEvent: ParseEvent) => {
        const event = inEvent as ParsedEvent
        const data = JSON.parse(event.data)
        const local_elements = {...elementsAndLookup}
        processEvent(data as ChatEvent, local_elements)
        updateElements(local_elements)
      })
      eventSourceParser.feed(chunk)
    } catch (error) {
      console.error('Error parsing data:', error);
    }
  };

  while (true) {
    const {done, value} = await reader.read();
    if (done) break;
    const chunk = decoder.decode(value, {stream: true});
    processChunk(chunk);
  }

}

export async function getChatEventInUI(processId: string) {
  const response = await fetch(`/api/eidolon/process/${processId}/events`, {
    method: "GET",
  })

  if (!response.ok) {
    return undefined
  }

  const events = (await response.json()) as ChatEvent[]
  const local_elements: ElementsAndLookup = {elements: [], lookup: {}}
  events.forEach(event => {
    processEvent(event, local_elements)
  })

  return local_elements
}
