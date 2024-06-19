import {Badge, Divider, IconButton, Paper, Typography} from "@mui/material";
import {ChooseLLMElement} from "../messages/choose-llm-element.tsx";
import {useSupportedLLMsOnOperation} from "../hooks/useSupportedLLMsOnOperation.ts";
import {useProcesses} from "../hooks/processes_context.tsx";
import {executeOperation} from "../client-api-helpers/process-event-helper.ts";
import {CopilotParams} from "../lib/util.ts";
import {CopilotInputForm, ProcessError, ProcessLoading, ProcessTerminated} from "./input_form_components.tsx";
import {FileHandle, ProcessStatus} from "@eidolon/client";
import ArticleOutlinedIcon from '@mui/icons-material/ArticleOutlined.js';
import {useEffect, useState} from "react";
import {getOperations} from "../client-api-helpers/machine-helper.ts";
import {useProcess} from "../hooks/process_context.tsx";

export interface CopilotInputPanelParams {
  machineUrl: string
  processId: string
  copilotParams: CopilotParams
  processState?: ProcessStatus
  // eslint-disable-next-line no-unused-vars
  executeAction: (machineUrl: string, agent: string, operation: string, payload: string | Record<string, any>) => Promise<void>
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
  const {selectedLLM, setSelectedLLM} = useSupportedLLMsOnOperation(machineUrl, copilotParams)
  const {updateProcesses} = useProcesses()
  const [uploadedFiles, setUploadedFiles] = useState<FileHandle[]>([]);
  const {app, processStatus} = useProcess()

  useEffect(() => {
    if (app && processStatus) {
      getOperations(processStatus!.machine, copilotParams.agent).then(operations => {
        const options = copilotParams
        const operation = operations.find((o) => o.name === options.operation)
        if (operation) {
          options.operationInfo = operation
          if (operation.schema?.properties?.execute_on_cpu) {
            const property = operation.schema?.properties?.execute_on_cpu as Record<string, any>
            options.supportedLLMs = property?.["enum"] as string[]
            options.defaultLLM = property?.default as string
          }
        }
      })
    }
  }, [app, processStatus]);

  const addUploadedFiles = (files: FileHandle[]) => {
    setUploadedFiles([...uploadedFiles, ...files]);
  }

  async function doAction(input: string) {
    let payload: string | Record<string, any> = {
      body: input
    }

    if (copilotParams.supportedLLMs && copilotParams.supportedLLMs.length > 0) {
      payload['execute_on_cpu'] = selectedLLM
    }

    if (uploadedFiles.length > 0) {
      payload['attached_files'] = uploadedFiles
    }

    if (!copilotParams.allowSpeech && Object.keys(payload).length === 1) {
      payload = payload['body']
    }

    if (processState?.state === "initialized" && copilotParams.titleOperationName) {
      // generate a title
      await executeOperation(machineUrl, copilotParams.agent, copilotParams.titleOperationName, processId, {body: input})
      updateProcesses(machineUrl).then()
    }

    await executeAction(machineUrl, copilotParams.agent, copilotParams.operation, payload)
    setUploadedFiles([])
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
                        addUploadedFiles={addUploadedFiles}
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
      {uploadedFiles && uploadedFiles.length > 0 && (
        <div style={{display: "flex", flexDirection: "row", height: "38px", alignItems: "center", justifyContent: "left", marginTop: "-38px", marginLeft: "-12px"}}>
          <Badge badgeContent={uploadedFiles.length} color="primary" sx={{height: "24px", width: "24px"}}>
            <IconButton sx={{height: "32px", width: "32px"}}
                        onClick={() => {

                        }}
                        style={{}}>
              <ArticleOutlinedIcon sx={{height: "32px", width: "32px"}}/>
            </IconButton>
          </Badge>
        </div>
      )}
      <div style={{display: "flex", flexDirection: "row", justifyContent: "space-between", marginLeft: "8px", marginRight: "8px"}}>
        <ChooseLLMElement supportedLLMs={copilotParams.supportedLLMs} selectedLLM={selectedLLM} setSelectedLLM={setSelectedLLM}/>
        <Typography sx={{marginBottom: "6px"}} alignSelf={"end"} variant={"caption"}>Press <b>Shift-Enter</b> to add a line</Typography>
      </div>
      <Divider sx={{marginTop: "-1px"}}/>
      <div style={{width: "100%", display: "flex", flexDirection: "row"}}>
        {content}
      </div>
    </Paper>
  )
}
