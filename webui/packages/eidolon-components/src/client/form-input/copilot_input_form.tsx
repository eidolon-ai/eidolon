'use client'

import {ChooseLLMElement} from "../messages/choose-llm-element.tsx";
import {useSupportedLLMsOnOperation} from "../hooks/useSupportedLLMsOnOperation.ts";
import {useProcesses} from "../hooks/processes_context.tsx";
import {executeOperation} from "../client-api-helpers/process-event-helper.ts";
import {CopilotParams} from "../lib/util.ts";
import {CopilotInputForm, ProcessError, ProcessLoading, ProcessTerminated} from "./input_form_components.tsx";
import {FileHandle, ProcessStatus} from "@eidolon-ai/client";
import {FileText} from 'lucide-react';
import {useEffect, useState} from "react";
import {getOperations} from "../client-api-helpers/machine-helper.ts";
import {useProcess} from "../hooks/process_context.tsx";
import {createProcess, deleteProcess} from "../client-api-helpers/process-helper.js";

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
          if (operation.schema?.properties?.execute_on_apu) {
            const property = operation.schema?.properties?.execute_on_apu as Record<string, any>
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
      payload['execute_on_apu'] = selectedLLM
    }

    if (uploadedFiles.length > 0) {
      payload['attached_files'] = uploadedFiles
    }

    if (!copilotParams.allowSpeech && Object.keys(payload).length === 1) {
      payload = payload['body']
    }

    if (processState?.state === "initialized" && copilotParams.titleOperationName) {
      // generate a title
      const processStatus = await createProcess(machineUrl, copilotParams.agent, copilotParams.titleOperationName)
      if (processStatus) {
        await executeOperation(machineUrl, copilotParams.agent, copilotParams.titleOperationName, processStatus.process_id, {body: input})
        await deleteProcess(machineUrl, processStatus.process_id)
      }
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
    <div className="w-full mb-8 p-4 pl-6 rounded-xl border-2 border-gray-100 border-solid flex flex-col bg-white">
      {uploadedFiles && uploadedFiles.length > 0 && (
        <div className="flex flex-row h-[38px] items-center justify-start -mt-[38px] -ml-3">
          <div className="flex items-center justify-center h-6 w-6 rounded-full bg-blue-500 text-white text-xs font-bold">
            {uploadedFiles.length}
          </div>
          <button
            className="p-1 rounded-full hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200"
            onClick={() => {
              // Your onClick logic here
            }}
          >
            <FileText className="h-8 w-8"/>
          </button>
        </div>
      )}
      <div className="flex flex-row justify-between mx-2">
        <ChooseLLMElement
          supportedLLMs={copilotParams.supportedLLMs}
          selectedLLM={selectedLLM}
          setSelectedLLM={setSelectedLLM}
        />
        <p className="text-xs self-end mb-1.5">
          Press <strong>Shift-Enter</strong> to add a line
        </p>
      </div>
      <hr className="border-t border-gray-200 -mt-px"/>
      <div className="w-full flex flex-row pt-1">{content}</div>
    </div>
  )
}
