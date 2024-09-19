'use client'

import {useProcessEvents} from "../hooks/useProcessEvents.ts";
import {EidolonEvents} from "../messages/eidolon-events.tsx";
import {AgentProcess} from "./agent-process.tsx";
import {useEidolonContext} from "../provider/eidolon_provider.tsx";
import {DevParams} from "../lib/util.ts";

export interface MessagesWithActionProps {
  machineUrl: string
  devParams: DevParams
  processId: string
  userImage?: string
  userName?: string
  scrollableRegionRef?: React.RefObject<HTMLDivElement>
}

export function DevPanel({machineUrl, devParams, processId, userName, userImage, scrollableRegionRef}: MessagesWithActionProps) {
  const [_, dispatch] = useEidolonContext()

  const {
    processState,
    elementsAndLookup,
    executeAction,
    handleCancel
  } = useProcessEvents(machineUrl, devParams.agent, processId, dispatch)

  return (
    <div className={"flex flex-col justify-between items-center overflow-hidden h-full w-full"}>
      <EidolonEvents scrollableRegionRef={scrollableRegionRef} machineUrl={machineUrl} agentName={devParams.agent} elementsAndLookup={elementsAndLookup}
                      userImage={userImage} userName={userName}
      />
      <AgentProcess operations={devParams.operations} processState={processState} handleAction={executeAction}
                    handleCancel={handleCancel}/>
    </div>
  )
}
