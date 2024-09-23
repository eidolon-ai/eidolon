import {createParser, ParsedEvent, ParseEvent} from "eventsource-parser";
import {ChatEvent} from "@eidolon-ai/client";

export async function executeOperation(machineUrl: string, agent: string, operation: string, processId: string,
                                       data: string | Record<string, unknown>) {
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

export async function streamOperation(machineUrl: string, agent: string, operation: string, processId: string, data: Record<string, unknown>,
                                       
                                      handleEvent: (data: Record<string, unknown>) => void,
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

   
  while (true) {
    const {done, value} = await reader.read();
    if (done) break;
    const chunk = decoder.decode(value, {stream: true});
    processChunk(chunk);
  }
}

export async function executeServerOperation(machineUrl: string, agent: string, operation: string, processId: string,
                                             data: unknown | Record<string, unknown>,
                                             processEvent: (event: ChatEvent) => void,
                                             cancelFetchController: AbortController) {
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
        processEvent(data as ChatEvent)
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

export async function getChatEventInUI(machineUrl: string, processId: string, processEvent: (event: ChatEvent) => void) {
  const response = await fetch(`/api/eidolon/process/${processId}/events?machineURL=${machineUrl}`, {
    method: "GET"
  })

  if (!response.ok) {
    return undefined
  }

  const events = (await response.json()) as ChatEvent[]
  events.forEach(event => {
    processEvent(event)
  })
}
