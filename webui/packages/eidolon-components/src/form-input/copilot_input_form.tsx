import {Divider, Paper, Typography} from "@mui/material";
import {ChooseLLMElement} from "../messages/choose-llm-element";
import {useSupportedLLMsOnOperation} from "../hooks/useSupportedLLMsOnOperation";
import {useProcesses} from "../hooks/process_context";
import {executeOperation} from "../client-api-helpers/process-event-helper";
import {CopilotParams} from "../lib/util";
import {CopilotInputForm, ProcessError, ProcessLoading, ProcessTerminated} from "./input_form_components";
import {ProcessStatus} from "@eidolon/client";

export interface CopilotInputPanelParams {
  machineUrl: string
  processId: string
  copilotParams: CopilotParams
  processState?: ProcessStatus
  executeAction: (machineUrl: string, agent: string, operation: string, payload: Record<string, any>) => Promise<void>
  handleCancel: () => void
}

export function CopilotInputPanel({
                                    machineUrl,
                                    processId,
                                    copilotParams,
                                    processState,
                                    executeAction,
                                    handleCancel
                                  }: CopilotInputPanelParams) {
  const {supportedLLMs, selectedLLM, setSelectedLLM} = useSupportedLLMsOnOperation(machineUrl, copilotParams.agent, copilotParams.operation)
  const {updateProcesses} = useProcesses()

  async function doAction(input: string) {
    const payload: Record<string, any> = {
      body: input
    }

    if (supportedLLMs && supportedLLMs.length > 0) {
      payload['execute_on_cpu'] = selectedLLM
    }

    if (processState?.state === "initialized" && copilotParams.titleOperationName) {
      // generate a title
      await executeOperation(machineUrl, copilotParams.agent, copilotParams.titleOperationName, processId, {body: input})
      updateProcesses(machineUrl).then()
    }
    await executeAction(machineUrl, copilotParams.agent, copilotParams.operation, payload)
  }

  let content: JSX.Element
  if (!processState) {
    content = (
      <ProcessLoading/>
    )
  } else if ((processState?.state === 'http_error' || processState?.state === 'error' || processState?.state === 'unhandled_error') && processState?.available_actions?.length === 0) {
    content = (
      <ProcessError error={processState.error!}/>
    )
  } else if (processState?.available_actions?.length === 0) {
    content = (
      <ProcessTerminated/>
    )
  } else {
    content = (
      <CopilotInputForm machineUrl={machineUrl} processId={processId} isProcessing={processState?.state === "processing"}
                        copilotParams={copilotParams} doAction={doAction} doCancel={handleCancel}
      />
    )
  }

  return (
    <Paper
      sx={{
        width: "100%",
        marginBottom: "16px",
        paddingTop: "8px",
        paddingLeft: "16px",
        paddingRight: "8px",
        paddingBottom: "8px",
        borderRadius: "16px",
        borderStyle: "solid",
        borderColor: "lightblue",
        display: "flex",
        flexDirection: "column",
      }}
    >
      <div style={{display: "flex", flexDirection: "row", justifyContent: "space-between", marginLeft: "8px", marginRight: "8px"}}>
        <ChooseLLMElement supportedLLMs={supportedLLMs} selectedLLM={selectedLLM} setSelectedLLM={setSelectedLLM}/>
        <Typography sx={{marginBottom: "6px"}} alignSelf={"end"} variant={"caption"}>Press <b>Shift-Enter</b> to add a line</Typography>
      </div>
      <Divider sx={{marginTop: "-1px"}}/>
      <div style={{width: "100%", display: "flex", flexDirection: "row"}}>
        {content}
      </div>
    </Paper>
  )
}
