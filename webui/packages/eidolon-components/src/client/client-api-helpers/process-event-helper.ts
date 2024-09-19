import {DisplayElement, ElementsAndLookup, makeElement, MarkdownElement} from "../lib/display-elements.ts";
import {createParser, ParsedEvent, ParseEvent} from "eventsource-parser";
import {ChatEvent} from "@eidolon-ai/client";

const getLastStreamContext = (stream_context: string) => {
  const contextChain: string[] = stream_context.split(".")
  return contextChain[contextChain.length - 1]!
}

const processEvent = (event: ChatEvent, elements: ElementsAndLookup) => {
  const element = makeElement(event)
  if (element) {
    let lastElement: DisplayElement | undefined
    if (event.stream_context) {
      const lastContext = getLastStreamContext(event.stream_context)
      const parent = elements.lookup[lastContext]!
      lastElement = parent.children[parent.children.length - 1]
    } else if (elements.rootAgent) {
      lastElement = elements.rootAgent.children[elements.rootAgent.children.length - 1]
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
      } else if (element.type === "agent-state" && !event.stream_context) {
        elements.rootAgent = undefined
      }

      if (event.stream_context) {
        const lastContext = getLastStreamContext(event.stream_context)
        const parent = elements.lookup[lastContext]!
        parent.children.push(element)
      } else if (elements.rootAgent) {
        elements.rootAgent.children.push(element)
      } else {
        elements.elements.push(element)
        if (element.type === "agent-start") {
          elements.rootAgent = element
        }
      }
    }
  }
}

export async function executeOperation(machineUrl: string, agent: string, operation: string, processId: string,
                                       data: string | Record<string, any>) {
  const response = await fetch(`/api/eidolon/process/${processId}/events`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Accept": "application/json"
    },
    body: JSON.stringify({machineUrl, agent, operation, data: data}),
  })
  return await response.json()
}

export async function streamOperation(machineUrl: string, agent: string, operation: string, processId: string, data: Record<string, any>,
                                      // eslint-disable-next-line no-unused-vars
                                      handleEvent: (data: Record<string, any>) => void,
) {
  const response = await fetch(`/api/eidolon/process/${processId}/events`, {
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
        handleEvent(data)
      })
      eventSourceParser.feed(chunk)
    } catch (error) {
      console.error('Error parsing data:', error);
    }
  };

  // eslint-disable-next-line no-constant-condition
  while (true) {
    const {done, value} = await reader.read();
    if (done) break;
    const chunk = decoder.decode(value, {stream: true});
    processChunk(chunk);
  }
}

export async function executeServerOperation(machineUrl: string, agent: string, operation: string, processId: string,
                                             data: Record<string, any>, elementsAndLookup: ElementsAndLookup,
                                             // eslint-disable-next-line no-unused-vars
                                             updateElements: (elements: ElementsAndLookup) => void, cancelFetchController: AbortController) {
  const response = await fetch(`/api/eidolon/process/${processId}/events`, {
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

  // eslint-disable-next-line no-constant-condition
  while (true) {
    const {done, value} = await reader.read();
    if (done) break;
    const chunk = decoder.decode(value, {stream: true});
    processChunk(chunk);
  }
}

export async function getChatEventInUI(machineUrl: string, processId: string) {
  const response = await fetch(`/api/eidolon/process/${processId}/events?machineURL=${machineUrl}`, {
    method: "GET"
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
