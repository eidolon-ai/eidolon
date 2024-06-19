'use client'

import {Box} from "@mui/material";
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
}

export function DevPanel({machineUrl, devParams, processId, userName, userImage}: MessagesWithActionProps) {
  const [_, dispatch] = useEidolonContext()

  const {
    processState,
    elementsAndLookup,
    executeAction,
    handleCancel
  } = useProcessEvents(machineUrl, devParams.agent, processId, dispatch)

  return (
    <Box sx={{
      height: '100%',
      width: '65vw',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'space-between',
      alignItems: 'center'
    }}>
      <EidolonEvents machineUrl={machineUrl} agentName={devParams.agent} elementsAndLookup={elementsAndLookup}
                      userImage={userImage} userName={userName}
      />
      <AgentProcess operations={devParams.operations} processState={processState} handleAction={executeAction}
                    handleCancel={handleCancel}/>
    </Box>
  )
}
