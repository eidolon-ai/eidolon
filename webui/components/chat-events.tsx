'use client'

import {ChatEvent, OperationInfo, ProcessState} from "@/lib/types";
import {Avatar, Box, Divider} from "@mui/material";
import * as React from "react";
import {useEffect, useRef, useState} from "react";
import {
  AgentStartElement,
  DisplayElement,
  ElementsAndLookup,
  ErrorElement,
  JsonElement,
  makeElement,
  MarkdownElement,
  ToolCallElement,
  UserRequestElement
} from "@/lib/display-elements";
import "@/components/chat-events.css"
import {AgentProcess} from "@/components/agent-input/agent-process";
import {createParser, ParseEvent} from "eventsource-parser";
import {ParsedEvent} from "eventsource-parser/src/types";
import {useSession} from "next-auth/react";
import {EidolonMarkdown} from "@/components/eidolon-markdown";
import {ToolCall} from "@/components/tool-call-element";
import {ChatScrollAnchor} from "@/components/chat-scroll-anchor";
import {getChatEvents, getPIDStatus} from "@/app/api/chat/messages/chatHelpers";

interface ChatEventProps {
  agentName: string,
  processId: string,
}

export function ChatEvents({agentName, processId}: ChatEventProps) {
  const [elementsAndLookup, setElementsAndLookup] =
    useState<ElementsAndLookup>({elements: [], lookup: {}})
  const [processState, setProcessState] = useState<ProcessState | undefined>(undefined)
  const cancelFetchController = useRef<AbortController | null>();

  const processEvent = (event: ChatEvent, elements: ElementsAndLookup) => {
    const element = makeElement(event)
    if (element) {
      let lastElement: DisplayElement | undefined
      if (event.stream_context) {
        const parent = elements.lookup[event.stream_context]
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
          elements.lookup[element.contextId].is_active = false
        }
        if (event.stream_context) {
          const parent = elements.lookup[event.stream_context]
          parent.children.push(element)
        } else {
          elements.elements.push(element)
        }
      }
    }
  }

  function setAgentState() {
    getPIDStatus(agentName, processId).then((status) => {
      if (status) {
        setProcessState(status)
      }
    })
  }

  function getChatEventInUI() {
    getChatEvents(agentName, processId).then((events) => {
      setElementsAndLookup({elements: [], lookup: {}})
      console.log(elementsAndLookup)
      setProcessState(undefined)
      const local_elements: ElementsAndLookup = {elements: [], lookup: {}}
      events.forEach(event => {
        processEvent(event, local_elements)
      })
      setElementsAndLookup(local_elements)
    }).then(() => {
      setAgentState()
    })
  }

// First we fetch the chat events from the server
  useEffect(() => {
    getChatEventInUI();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [agentName, processId]);

  const handleCancel = () => {
    if (cancelFetchController.current) {
      cancelFetchController.current.abort();
      cancelFetchController.current = null;
    }
    getChatEventInUI();
  }

  const executeAction = async (operation: OperationInfo, data: Record<string, any>) => {
    setProcessState({state: "processing", available_actions: []});
    if (cancelFetchController.current) {
      cancelFetchController.current.abort();
    }
  
    cancelFetchController.current = new AbortController();
    try {
      // Call to the backend to decrement the user's token count
      const decrementTokenResponse = await fetch('/api/users', {
        method: 'PUT', // Use the PUT method as defined in your backend route
        headers: {
          'Content-Type': 'application/json',
        },
        // No need to send body data because user identification is handled via session in the backend
      });
  
      // Optional: Check response from decrement token call
      if (!decrementTokenResponse.ok) {
        throw new Error('Failed to decrement token');
      }
  
      const path = operation.path.replace("{process_id}", processId);
  
      const response = await fetch(`/api/chat/messages`, {
        signal: cancelFetchController.current.signal,
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Accept": "text/event-stream",
        },
        body: JSON.stringify({ path: path, data: data }),
      });
  
      const reader = response.body!.getReader();
      const decoder = new TextDecoder();
  
      const processChunk = (chunk: string) => {
        try {
          const eventSourceParser = createParser((inEvent: ParseEvent) => {
            const event = inEvent as ParsedEvent;
            const data = JSON.parse(event.data);
            const local_elements = { ...elementsAndLookup };
            processEvent(data as ChatEvent, local_elements);
            setElementsAndLookup(local_elements);
          });
          eventSourceParser.feed(chunk);
        } catch (error) {
          console.error('Error parsing data:', error);
        }
      };
  
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value, { stream: true });
        processChunk(chunk);
      }
  
      setAgentState();
    } catch (error) {
      console.error('Error:', error);
    } finally {
      if (cancelFetchController.current) {
        cancelFetchController.current.abort();
        cancelFetchController.current = null;
      }
      if (processState?.state === "processing") {
        setProcessState(undefined);
      }
    }
  };
  

  return (
    <Box sx={{
      height: '100%',
      width: '65vw',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'space-between',
      alignItems: 'center'
    }}>
      <Box id="chat-elements-scroll-region"
           sx={{overflowY: 'auto', overflowX: 'hidden', width: '60vw', marginBottom: '8px'}}>
        {elementsAndLookup.elements.map((child, index) => {
            if (index < elementsAndLookup.elements.length - 1 || child.type != "success") {
              return <ChatDisplayElement key={index} rawElement={child}
                                         topLevel={index == elementsAndLookup.elements.length - 1}
                                         agentName={agentName} handleAction={executeAction}/>
            }
          }
        )}
        <ChatScrollAnchor trackVisibility={true}></ChatScrollAnchor>
      </Box>
      <AgentProcess agent={agentName} processState={processState} handleAction={executeAction}
                    handleCancel={handleCancel}/>
    </Box>
  )
}

// @ts-ignore
export const ChatDisplayElement = ({rawElement, agentName, topLevel, handleAction}: {
  rawElement: DisplayElement, topLevel: boolean, agentName: string,
  handleAction: (operation: OperationInfo, data: Record<string, any>) => void
}) => {
  const {data: session} = useSession()
  const getUserInput = (element: UserRequestElement) => {
    // todo, make sure this renders file inputs correctly
    let content = {...element.content}
    delete content["process_id"]
    if (Object.keys(content).length === 0) {
      return "*No Input*"
    } else if (Object.keys(content).length === 1) {
      content = content[Object.keys(content)[0]]
    }
    content = JSON.stringify(content, undefined, "  ")
    return '```json\n' + content + "\n```"
  }

  switch (rawElement.type) {
    case "agent-start": {
      const element = rawElement as AgentStartElement
      return (
        <div>
          <div className={"chat-title"}><Avatar sx={{height: "36px", width: "36px"}} src="/eidolon_with_gradient.png"/>
            <span style={{marginLeft: '8px'}}>{element.agentName} started action {element.callName}</span></div>
        </div>
      )
    }
    case "user-request": {
      const element = rawElement as UserRequestElement
      return (
        <div>
          <div className={"chat-title"}>{topLevel ?
            <Avatar sx={{height: "32px", width: "32px"}} src={session?.user?.image!}/> :
            <Avatar sx={{height: "36px", width: "36px"}} src="/eidolon_with_gradient.png"/>}
            <span style={{marginLeft: '8px'}}>{topLevel ? "User" : "Agent Input"}</span></div>
          <div className={"chat-indent"}>
            <EidolonMarkdown>{getUserInput(element)}</EidolonMarkdown>
          </div>
        </div>
      )
    }
    case "markdown": {
      const element = rawElement as MarkdownElement
      return (
        <div className={"chat-indent"}>
          <EidolonMarkdown>{element.content}</EidolonMarkdown>
        </div>
      )
    }
    case "json": {
      const element = rawElement as JsonElement
      return (
        <div className={"chat-indent"}>
          <EidolonMarkdown>{'```json\n' + JSON.stringify(element.content, undefined,
            "  ") + "\n```"}</EidolonMarkdown>
        </div>
      )
    }
    case "tool-call": {
      const element = rawElement as ToolCallElement
      return (
        <div className={"chat-indent"}>
          <ToolCall element={element} agentName={agentName} handleAction={handleAction}/>
        </div>
      )
    }
    case "success": {
      return (
        <Divider sx={{margin: "16px 0 16px 0"}} variant={"middle"}/>
      )
    }
    case "error": {
      const element = rawElement as ErrorElement
      return (
        <div>
          <span className={"chat-title"}>Error</span>
          <div className={"chat-indent"}>
            <EidolonMarkdown>{element.reason}</EidolonMarkdown>
          </div>
        </div>
      )
    }
    case "canceled": {
      return (
        <div>
          <span className={"chat-canceled"}>Operation Canceled or Interrupted</span>
        </div>
      )
    }
  }
}
