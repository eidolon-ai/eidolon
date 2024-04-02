import {notFound} from "next/navigation";
import * as React from "react";
import {MessagesWithSingleAction} from "@eidolon/components/src/form-input/MessagesWithSingleAction";
import {CopilotParams, getApp} from "@/utils/eidolon-apps";
import {_processHandler} from "../../../../api/eidolon/eidolon_helpers";

export interface ProcessPageProps {
  params: {
    app_name: string
    processId: string
  }
}

export default async function ({params}: ProcessPageProps) {
  let app = getApp(params.app_name)!
  const options = app.params as CopilotParams

  const machineUrl = app.location!
  const processStatus = await _processHandler.getProcess(machineUrl, params.processId)
  if (!processStatus) {
    notFound()
  }

  return (
    <MessagesWithSingleAction
      machineUrl={processStatus.machine}
      agent={processStatus.agent}
      processId={processStatus.process_id}
      operationName={options.operation}
      titleOperationName={options.titleOperationName}
      inputLabel={options.inputLabel}
      allowSpeech={options.allowSpeech}
      speechAgent={options.speechAgent}
      speechOperation={options.speechOperation}
    />
  )
}
