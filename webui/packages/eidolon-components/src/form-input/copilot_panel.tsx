'use client'

import {Box, Theme} from "@mui/material";
import {EidolonEvents} from "../messages/eidolon-events";
import {ButtonScrollToBottom} from "./button-scroll-to-bottom";
import {CopilotInputPanel} from "./copilot_input_form";
import {useProcessEvents} from "../hooks/useProcessEvents";
import {CopilotParams} from "../lib/util";
import {useEidolonContext} from "../provider/eidolon_provider";
import "./copilot-panel.css"
import {SxProps} from "@mui/material/styles";

export interface CopilotPanelParams {
  machineUrl: string
  processId: string
  copilotParams: CopilotParams
  userImage: string | null | undefined
  userName: string | null  | undefined
  // eslint-disable-next-line no-unused-vars
  afterExecute?: (payload: string | Record<string, any>) => void
  sx?: SxProps<Theme>;
}

export function CopilotPanel({machineUrl, processId, copilotParams, userName, userImage, afterExecute, sx}: CopilotPanelParams) {
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
    <Box
      className={"copilot-panel"}
      sx={{
      height: '100%',
      width: '100%',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'space-between',
      alignItems: 'center',
      overflow: "hidden",
        ...sx
    }}>
      <EidolonEvents machineUrl={machineUrl} agentName={copilotParams.agent} elementsAndLookup={elementsAndLookup}
                     userImage={userImage} userName={userName}
      />
      <div style={{textAlign: "right", width: "100%", height: "32px", marginRight: "35px"}}>
        <ButtonScrollToBottom/>
      </div>
      <CopilotInputPanel machineUrl={machineUrl} processId={processId} copilotParams={copilotParams}
                         processState={processState} executeAction={doExecute} handleCancel={handleCancel}
      />
    </Box>
  )
}
