'use client'

import {Box} from "@mui/material";
import {EidolonEvents} from "../messages/eidolon-events";
import {ButtonScrollToBottom} from "./button-scroll-to-bottom";
import {CopilotInputPanel} from "./copilot_input_form";
import {useProcessEvents} from "../hooks/useProcessEvents";
import {CopilotParams} from "../lib/util";
import {useEidolonContext} from "../provider/eidolon_provider";

export interface CopilotPanelParams {
  machineUrl: string
  processId: string
  copilotParams: CopilotParams
}

export function CopilotPanel({machineUrl, processId, copilotParams}: CopilotPanelParams) {
  const [_, dispatch] = useEidolonContext()
  const {
    elementsAndLookup,
    processState,
    executeAction,
    handleCancel
  } = useProcessEvents(machineUrl, copilotParams.agent, processId, dispatch)

  return (
    <Box sx={{
      height: '100%',
      width: '65vw',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'space-between',
      alignItems: 'center',
      overflow: "hidden"
    }}>
      <EidolonEvents machineUrl={machineUrl} agentName={copilotParams.agent} elementsAndLookup={elementsAndLookup}
      />
      <div style={{textAlign: "right", width: "100%", height: "32px", marginRight: "35px"}}>
        <ButtonScrollToBottom/>
      </div>
      <CopilotInputPanel machineUrl={machineUrl} processId={processId} copilotParams={copilotParams}
                         processState={processState} executeAction={executeAction} handleCancel={handleCancel}
      />
    </Box>
  )
}
