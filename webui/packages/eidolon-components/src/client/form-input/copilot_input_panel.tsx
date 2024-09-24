'use client'

import {CopilotInputForm, ProcessError, ProcessLoading, ProcessTerminated} from "./copilot_input_form.tsx";
import {useEffect, useRef, useState} from "react";
import {getOperations} from "../client-api-helpers/machine-helper.ts";
import {SelectedFile} from "../file-upload/file-upload.js";
import {CopilotParams} from "../lib/util.js";
import {uploadFiles} from "../client-api-helpers/files-helper.js";
import {ProcessStatus} from "@eidolon-ai/client";
import {NewChatOptions} from "eidolon-ui2/app/eidolon-apps/sp/[app_name]/new-chat-options.js";

export interface CopilotInputPanelParams {
  machineUrl: string,
  copilotParams: CopilotParams,
  processState: ProcessStatus | undefined,
  executeAction: (operation: string, payload: string | Record<string, any>) => Promise<void>;
  handleCancel: () => void
  options?: NewChatOptions
  clearOptions: () => void
}

export function CopilotInputPanel({
                                    machineUrl,
                                    copilotParams,
                                    processState,
                                    executeAction,
                                    handleCancel,
                                    options,
                                    clearOptions
                                  }: CopilotInputPanelParams) {
  const [supportedLLMs, setSupportedLLMs] = useState<string[] | undefined>()
  const [selectedLLM, setSelectedLLM] = useState<string | undefined>()
  const hasRun = useRef(false);

  useEffect(() => {
    if (hasRun.current) return;
    if (options) {
      hasRun.current = true;
      const input = options.input;
      const inFiles = options.files;
      const selectedLLM = options.selectedLLM;
      clearOptions();
      doAction(input, inFiles, selectedLLM).then(() => {
        hasRun.current = false;  // Reset for next update if needed
      })
    }
  }, [options, executeAction]);

  async function doAction(input: string, inFiles: SelectedFile[], selectedLLM?: string) {
    const files = await uploadFiles(machineUrl, processState!.process_id, inFiles)

    let payload: string | Record<string, any> = {
      body: input
    }

    if (supportedLLMs && supportedLLMs?.length > 0) {
      console.log("+++++here", selectedLLM)
      payload['execute_on_apu'] = selectedLLM
    }

    if (files.length > 0) {
      payload['attached_files'] = files
    }

    if (!copilotParams.allowSpeech && Object.keys(payload).length === 1) {
      payload = payload['body']
    }

    await executeAction(copilotParams.operation, payload)
  }

  useEffect(() => {
    if (copilotParams) {
      getOperations(machineUrl, copilotParams.agent).then(operations => {
        const operation = operations.find((o) => o.name === copilotParams.operation)
        if (operation) {
          copilotParams.operationInfo = operation
          if (operation.schema?.properties?.execute_on_apu) {
            const property = operation.schema?.properties?.execute_on_apu as Record<string, any>
            setSupportedLLMs(property?.["enum"] as string[])
            setSelectedLLM(property?.default as string)
          }
        }
      })
    }
  }, [copilotParams]);

  let content: JSX.Element
  if (!processState) {
    content = (
      <ProcessLoading/>
    )
  } else if ((processState?.state === 'http_error' || processState?.state === 'error' || processState?.state === 'unhandled_error') && processState?.available_actions?.length === 0) {
    content = (
      <ProcessError error={processState.error!}/>
    )
  } else if (processState.state !== "processing" && processState?.available_actions?.length === 0) {
    content = (
      <ProcessTerminated/>
    )
  } else {
    content =
      <CopilotInputForm doAction={doAction} handleCancel={handleCancel}
                        inputLabel={copilotParams?.inputLabel}
                        processState={processState?.state}
                        supportedLLMs={supportedLLMs}
                        selectedLLM={selectedLLM}
                        setSelectedLLM={setSelectedLLM}
                        speechOptions={copilotParams?.speechAgent && copilotParams?.speechOperation ? {
                          machineUrl: machineUrl,
                          agent: copilotParams?.speechAgent,
                          operation: copilotParams?.speechOperation,
                        } : undefined}
      />
  }

  return (
    <>
      {content}
    </>
  )
}
