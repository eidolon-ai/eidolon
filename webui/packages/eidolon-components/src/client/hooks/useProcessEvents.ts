import {useRef, useState} from "react";
import {DisplayElement, ElementsAndLookup, makeElement, MarkdownElement} from "../lib/display-elements.ts";
import {executeServerOperation, getChatEventInUI} from "../client-api-helpers/process-event-helper.ts";
import {useApp} from "./app-context.js";
import {useProcess} from "./process_context.js";
import {ChatEvent} from "@eidolon-ai/client";

export function useProcessEvents() {
  const cancelFetchController = useRef<AbortController | null>();
  const [elementsAndLookup, setElementsAndLookup] =
    useState<ElementsAndLookup>({elements: [], lookup: {}})

  const {app} = useApp()
  const {processStatus, updateProcessStatus} = useProcess()

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
          updateProcessStatus().then()
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
            updateProcessStatus().then()
          }
        }
      }
    }
  }

  function loadChatEvents() {
    if (app && processStatus) {
      const localElements = {elements: [], lookup: {}}
      setElementsAndLookup({elements: [], lookup: {}})
      getChatEventInUI(app?.location, processStatus.process_id, (event) => {
        processEvent(event, localElements)
      }).then(() => {
        setElementsAndLookup(localElements)
      }).catch(error => {
        console.error('Error fetching chat events:', error);
      })
    }
  }

  const executeAction = async (operation: string, data: unknown) => {
    if (!app || !processStatus) {
      return
    }
    if (cancelFetchController.current) {
      cancelFetchController.current.abort();
    }
    cancelFetchController.current = new AbortController();
    try {
      let local_elements = {...elementsAndLookup}
      await executeServerOperation(app.location, processStatus.agent, operation, processStatus.process_id, data,
        (event) => {
          local_elements = {...local_elements}
          processEvent(event as ChatEvent, local_elements)
          setElementsAndLookup(local_elements)
        }, cancelFetchController.current)
      cancelFetchController.current = null;
    } catch (error) {
      console.error('Error executing action:', error);
      if (cancelFetchController.current) {
        cancelFetchController.current.abort();
        cancelFetchController.current = null;
      }
    }
  }

  const handleCancel = () => {
    if (cancelFetchController.current) {
      cancelFetchController.current.abort();
      cancelFetchController.current = null;
    }
    loadChatEvents();
  }

  return {
    loadChatEvents,
    elementsAndLookup,
    executeAction,
    handleCancel
  }
}