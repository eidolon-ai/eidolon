'use client'

import {Box} from "@mui/material";
import * as React from "react";
import {useEffect, useRef, useState} from "react";
import {ElementsAndLookup} from "../lib/display-elements.js";
import "./eidolon-events.css"
import {AgentProcess} from "../form-input/agent-process.js";
import {ChatScrollAnchor} from "./chat-scroll-anchor.js";
import {ChatDisplayElement} from "./chat-display-element.js";
import {executeServerOperation, getChatEventInUI} from "../client-api-helpers/process-event-helper.js";
import {OperationInfo, ProcessStatus} from "@eidolon/client"
import {getProcessStatus} from "../client-api-helpers/process-helper.js";

interface ChatEventProps {
  agentName: string,
  processId: string,
}

export function EidolonEvents({agentName, processId}: ChatEventProps) {
  const [elementsAndLookup, setElementsAndLookup] =
    useState<ElementsAndLookup>({elements: [], lookup: {}})
  const [processState, setProcessState] = useState<ProcessStatus | undefined>(undefined)
  const cancelFetchController = useRef<AbortController | null>();

  function setAgentState() {
    getProcessStatus(processId).then((status) => {
      if (status) {
        setProcessState(status)
      }
    })
  }

  function getChatEvents() {
    setElementsAndLookup({elements: [], lookup: {}})
    setProcessState(undefined)
    getChatEventInUI(processId).then((elements) => {
      if (elements) {
        setElementsAndLookup(elements)
      }
      setAgentState()
    })
  }

// First we fetch the chat events from the server
  useEffect(() => {
    getChatEvents();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [agentName, processId]);

  const handleCancel = () => {
    if (cancelFetchController.current) {
      cancelFetchController.current.abort();
      cancelFetchController.current = null;
    }
    getChatEvents();
  }

  const executeAction = async (operation: OperationInfo, data: Record<string, any>) => {
    setProcessState(undefined)
    if (cancelFetchController.current) {
      cancelFetchController.current.abort();
    }

    cancelFetchController.current = new AbortController();
    try {
      const path = operation.path.replace("{process_id}", processId)
      await executeServerOperation(operation.machine, operation.agent, operation.name, processId, data, elementsAndLookup, setElementsAndLookup, cancelFetchController.current)

      setAgentState();
      cancelFetchController.current = null;
    } catch (error) {
      console.error('Error fetching SSE stream:', error);
      if (cancelFetchController.current) {
        cancelFetchController.current.abort();
        cancelFetchController.current = null;
      }
    } finally {
      if (processState?.state === "processing") {
        setProcessState(undefined)
      }
    }
  }

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
