'use client'

import {useEffect, useRef, useState} from "react";
import {ProcessStatus} from "@eidolon/client";
import {ElementsAndLookup} from "../lib/display-elements";
import {executeServerOperation, getChatEventInUI} from "../client-api-helpers/process-event-helper";
import {getProcessStatus} from "../client-api-helpers/process-helper";
import {EidolonEvent, RecordUsage} from "../provider/eidolon_provider";

export function useProcessEvents(machineUrl: string, agent: string, processId: string,
                                 // eslint-disable-next-line no-unused-vars
                                 usageUpdateEvent: (event: EidolonEvent) => void
) {
  const [processState, setProcessState] = useState<ProcessStatus | undefined>(undefined)
  const cancelFetchController = useRef<AbortController | null>();
  const [elementsAndLookup, setElementsAndLookup] =
    useState<ElementsAndLookup>({elements: [], lookup: {}})

  const updateElements = (elements: ElementsAndLookup) => {
    usageUpdateEvent(RecordUsage)
    setElementsAndLookup(elements)
  }

  function getChatEvents() {
    updateElements({elements: [], lookup: {}})
    setProcessState(undefined)
    getChatEventInUI(machineUrl, processId).then((elements) => {
      if (elements) {
        updateElements(elements)
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