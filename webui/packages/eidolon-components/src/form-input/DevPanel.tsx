'use client'

import {Box} from "@mui/material";
import {useProcessEvents} from "../hooks/useProcessEvents";
import {EidolonEvents} from "../messages/eidolon-events";
import {AgentProcess} from "./agent-process";
import {useEidolonContext} from "../provider/eidolon_provider";
import {DevParams} from "../lib/util";

export interface MessagesWithActionProps {
  machineUrl: string
  devParams: DevParams
  processId: string
}

export function DevPanel({machineUrl, devParams, processId}: MessagesWithActionProps) {
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
      <EidolonEvents agentName={devParams.agent} elementsAndLookup={elementsAndLookup}/>
      <AgentProcess operations={devParams.operations} processState={processState} handleAction={executeAction}
                    handleCancel={handleCancel}/>
    </Box>
  )
}
