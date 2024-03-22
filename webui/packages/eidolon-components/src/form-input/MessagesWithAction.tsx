'use client'

import {Box} from "@mui/material";
import {useProcessEvents} from "../hooks/useProcessEvents";
import {EidolonEvents} from "../messages/eidolon-events";
import {AgentProcess} from "./agent-process";

export interface MessagesWithActionProps {
  machineUrl: string
  agent: string
  processId: string
}

export function MessagesWithAction({machineUrl, agent, processId}: MessagesWithActionProps) {
  const {
    processState,
    elementsAndLookup,
    executeAction,
    handleCancel
  } = useProcessEvents(machineUrl, agent, processId)

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
      <EidolonEvents agentName={agent} elementsAndLookup={elementsAndLookup}/>
      <AgentProcess agent={agent} processState={processState} handleAction={executeAction}
                    handleCancel={handleCancel}/>
    </Box>
  )
}
