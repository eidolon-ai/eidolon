'use client'

import {EidolonEvents} from "../messages/eidolon-events.tsx";
import {ButtonScrollToBottom} from "./button-scroll-to-bottom.tsx";
import {CopilotInputPanel} from "./copilot_input_form.tsx";
import {useProcessEvents} from "../hooks/useProcessEvents.ts";
import {CopilotParams, DevParams} from "../lib/util.ts";
import {useEidolonContext} from "../provider/eidolon_provider.tsx";
import "./copilot-panel.css"
import {AgentProcess} from "./agent-process.js";

export interface CopilotPanelParams {
  machineUrl: string
  processId: string
  copilotParams: CopilotParams | DevParams
  userImage: string | null | undefined
  userName: string | null | undefined
  // eslint-disable-next-line no-unused-vars
  afterExecute?: (payload: string | Record<string, any>) => void
  scrollableRegionRef?: React.RefObject<HTMLDivElement>
}

export function CopilotPanel({machineUrl, processId, copilotParams, userName, userImage, afterExecute, scrollableRegionRef}: CopilotPanelParams) {
  const [_, dispatch] = useEidolonContext()
  const {
    elementsAndLookup,
    processState,
    executeAction,
    handleCancel
  } = useProcessEvents(machineUrl, copilotParams.agent, processId, dispatch)

  function doExecute(machineUrl: string, agent: string, operation: string, payload: string | Record<string, any>) {
    return executeAction(machineUrl, agent, operation, payload).then(() => {
      if (afterExecute) {
        afterExecute(payload)
      }
    })
  }

  return (
    <div
      className={"copilot-panel flex flex-col justify-between items-center overflow-hidden h-full w-full"}
    >
      <EidolonEvents scrollableRegionRef={scrollableRegionRef} machineUrl={machineUrl} agentName={copilotParams.agent} elementsAndLookup={elementsAndLookup}
                     userImage={userImage} userName={userName}
      />
      <div style={{textAlign: "right", width: "100%", height: "32px", marginRight: "35px"}}>
        <ButtonScrollToBottom/>
      </div>
      {copilotParams.type === "copilot" && copilotParams.operationInfo && (
        <CopilotInputPanel machineUrl={machineUrl} processId={processId} copilotParams={copilotParams}
                           processState={processState} executeAction={doExecute} handleCancel={handleCancel}
        />
      )}
      {copilotParams.type === "dev" && (
        <AgentProcess operations={copilotParams.operations} processState={processState} handleAction={executeAction} handleCancel={handleCancel}/>
      )}
    </div>
  )
}
