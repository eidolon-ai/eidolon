'use client'

import {useEffect, useRef, useState} from "react";
import {ProcessStatus} from "@eidolon/client";
import {AgentStateElement, ElementsAndLookup} from "../lib/display-elements";
import {executeServerOperation, getChatEventInUI} from "../client-api-helpers/process-event-helper";
import {getProcessStatus} from "../client-api-helpers/process-helper";
import {useProcesses} from "./process_context";

export function useProcessEvents(machineUrl: string, agent: string, processId: string) {
  const [processState, setProcessState] = useState<ProcessStatus | undefined>(undefined)
  const cancelFetchController = useRef<AbortController | null>();
  const [elementsAndLookup, setElementsAndLookup] =
    useState<ElementsAndLookup>({elements: [], lookup: {}})
  const {updateProcesses} = useProcesses()

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

  const executeAction = async (machine: string, agent: string, operation: string, data: any) => {
    setProcessState({...processState, state: "processing"} as ProcessStatus)
    if (cancelFetchController.current) {
      cancelFetchController.current.abort();
    }

    cancelFetchController.current = new AbortController();
    try {
      let lastProcessEvent = elementsAndLookup.elements.length
      const updateElements = (elements: ElementsAndLookup) => {
        const titleElements = elements.elements.slice(lastProcessEvent).filter((element) => element.type === "agent-state").map((element) => element as AgentStateElement)
          .filter((element) => element.title)
        if (titleElements.length > 0) {
          updateProcesses(machineUrl)
        }
        lastProcessEvent = elements.elements.length
        setElementsAndLookup(elements)
      }
      await executeServerOperation(machine, agent, operation, processId, data, elementsAndLookup, updateElements, cancelFetchController.current)
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

  return {
    processState,
    elementsAndLookup,
    executeAction,
    handleCancel
  }

}