'use client'

import {Box} from "@mui/material";
import {useProcessEvents} from "../hooks/useProcessEvents";
import {EidolonEvents} from "../messages/eidolon-events";
import {AgentProcess} from "./agent-process";
import {OperationInfo} from "@eidolon/client";

export interface MessagesWithActionProps {
  operations: OperationInfo[]
  machineUrl: string
  agent: string
  processId: string
}

export function MessagesWithAction({operations, machineUrl, agent, processId}: MessagesWithActionProps) {
  const {
    processState,
    elementsAndLookup,
    executeAction,
    handleCancel
  } = useProcessEvents(machineUrl, agent, processId)

  return (
    <Box sx={{
      height: '100%',
      width: '65vw',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'space-between',
      alignItems: 'center'
    }}>
      <EidolonEvents agentName={agent} elementsAndLookup={elementsAndLookup}/>
      <AgentProcess operations={operations} processState={processState} handleAction={executeAction}
                    handleCancel={handleCancel}/>
    </Box>
  )
}
