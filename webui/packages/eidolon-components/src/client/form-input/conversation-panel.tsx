'use client'

import {EidolonEvents} from "../messages/eidolon-events.tsx";
import {ButtonScrollToBottom} from "./button-scroll-to-bottom.tsx";
import {CopilotInputPanel} from "./copilot_input_panel.tsx";
import {useProcessEvents} from "../hooks/useProcessEvents.ts";
import {CopilotParams, DevParams} from "../lib/util.ts";
import "./conversation-panel.css"
import {AgentProcess} from "./agent-process.js";
import {NewChatOptions} from "eidolon-ui2/app/eidolon-apps/sp/[app_name]/new-chat-options.js";
import {useProcess} from "../hooks/process_context.js";
import {useEffect, useRef} from "react";

export interface CopilotPanelParams {
  machineUrl: string
  agent: string
  processId: string
  copilotParams: CopilotParams | DevParams
  userImage: string | null | undefined
  userName: string | null | undefined
  afterExecute?: (payload: string | Record<string, any>) => void
  scrollableRegionRef: React.RefObject<HTMLDivElement>
  operation?: string
  handleNewConversation: () => void
  options?: NewChatOptions
  clearOptions: () => void
  goToProcess: (processId: string) => void;
}

export function ConversationPanel({
                                    machineUrl, agent, goToProcess, copilotParams, userName, userImage, afterExecute,
                                    scrollableRegionRef, operation, handleNewConversation,
                                    options, clearOptions
                                  }: CopilotPanelParams) {
  const {
    elementsAndLookup,
    loadChatEvents,
    executeAction,
    handleCancel
  } = useProcessEvents()
  const {processStatus} = useProcess()
  const effectRan = useRef(false);

  useEffect(() => {
    if (processStatus !== undefined && !effectRan.current) {
      if (!options) {
        loadChatEvents()
      }
      effectRan.current = true;
    }
  }, [processStatus]);

  const doExecute = async (operation: string, payload: string | Record<string, any>) => {
    await executeAction(operation, payload).then(() => {
      if (afterExecute) {
        afterExecute(payload)
      }
    });
  }

  return (
    <div
      className={"copilot-panel flex flex-col justify-between items-center overflow-hidden h-full w-full"}
    >
      <ButtonScrollToBottom/>
      <EidolonEvents scrollableRegionRef={scrollableRegionRef} agentName={agent} elementsAndLookup={elementsAndLookup}
                     userImage={userImage} userName={userName} goToProcess={goToProcess}
      />
      {copilotParams.type === "copilot" && copilotParams.operationInfo && processStatus && (
        <div className={"w-full flex flex-col rounded-t-xl border-solid border-gray-200 "}>
          <CopilotInputPanel machineUrl={machineUrl} copilotParams={copilotParams} processState={processStatus}
                             executeAction={doExecute} handleCancel={handleCancel}
                             options={options} clearOptions={clearOptions}
          />
        </div>
      )}
      {copilotParams.type === "dev" && (
        <AgentProcess selectedOperation={operation} handleAction={doExecute} handleCancel={handleCancel}
                      handleNewConversation={handleNewConversation}
        />
      )}
    </div>
  )
}
