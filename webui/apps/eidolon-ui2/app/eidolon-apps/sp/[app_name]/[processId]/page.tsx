import {notFound} from "next/navigation";
import * as React from "react";
import {MessagesWithSingleAction} from "@eidolon/components/src/form-input/MessagesWithSingleAction";
import {getApp} from "@/utils/eidolon-apps";
import {_processHandler} from "../../../../api/eidolon/eidolon_helpers";

export interface ProcessPageProps {
  params: {
    app_name: string
    processId: string
  }
}

export default async function ({params}: ProcessPageProps) {
  const machineUrl = getApp(params.app_name)?.location!
  const processStatus = await _processHandler.getProcess(machineUrl, params.processId)
  if (!processStatus) {
    notFound()
  }

  return (
    <MessagesWithSingleAction
      machineUrl={processStatus.machine}
      agent={processStatus.agent}
      processId={processStatus.process_id}
      operationName={"converse"}
      titleOperationName={"generate_title"}
      inputLabel={"How can I help you?"}
      allowSpeech={true}
      speechAgent={"speech_agent"}
      speechOperation={"speech_to_text"}
    />
  )
}
