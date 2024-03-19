'use client'

import {Box} from "@mui/material";
import {OperationInfo, ProcessStatus} from "@eidolon/client";
import {useEffect, useRef, useState} from "react";
import {ElementsAndLookup} from "../lib/display-elements";
import {executeServerOperation, getChatEventInUI} from "../client-api-helpers/process-event-helper";
import {EidolonEvents} from "./eidolon-events";
import {AgentProcess} from "../form-input/agent-process";
import {getProcessStatus} from "../client-api-helpers/process-helper";

export interface MessagesWithActionProps {
  machineUrl: string
  agent: string
  processId: string
}

export function MessagesWithAction({machineUrl, agent, processId}: MessagesWithActionProps) {
  const [processState, setProcessState] = useState<ProcessStatus | undefined>(undefined)
  const cancelFetchController = useRef<AbortController | null>();
  const [elementsAndLookup, setElementsAndLookup] =
    useState<ElementsAndLookup>({elements: [], lookup: {}})

  function getChatEvents() {
    setElementsAndLookup({elements: [], lookup: {}})
    setProcessState(undefined)
    getChatEventInUI(machineUrl, processId).then((elements) => {
      if (elements) {
        setElementsAndLookup(elements)
      }
      setAgentState()
    })
  }

// First we fetch the chat events from the server
  useEffect(() => {
    getChatEvents();
  }, [agent, processId]);

  function setAgentState() {
    getProcessStatus(machineUrl, processId).then((status) => {
      if (status) {
        setProcessState(status)
      }
    })
  }
  const executeAction = async (operation: OperationInfo, data: Record<string, any>) => {
    setProcessState(undefined)
    if (cancelFetchController.current) {
      cancelFetchController.current.abort();
    }

    cancelFetchController.current = new AbortController();
    try {
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

  const handleCancel = () => {
    if (cancelFetchController.current) {
      cancelFetchController.current.abort();
      cancelFetchController.current = null;
    }
    getChatEvents();
  }

  // todo -- move all of the stuff here into a hook that initializes this mess and returns the elementsAndLookup handle + execute action + handle cancel
  return (
    <Box sx={{
      height: '100%',
      width: '65vw',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'space-between',
      alignItems: 'center'
    }}>
      <EidolonEvents agentName={agent} elementsAndLookup={elementsAndLookup} handleAction={executeAction}/>
      <AgentProcess agent={agent} processState={processState} handleAction={executeAction}
                    handleCancel={handleCancel}/>
    </Box>
  )
}
