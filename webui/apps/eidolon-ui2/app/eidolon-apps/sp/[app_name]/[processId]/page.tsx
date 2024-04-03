import {notFound} from "next/navigation";
import * as React from "react";
import {CopilotPanel} from "@eidolon/components/src/form-input/copilot_panel";
import {getApp} from "@/utils/eidolon-apps";
import {_processHandler} from "../../../../api/eidolon/eidolon_helpers";
import {CopilotParams} from "@eidolon/components";

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
    <CopilotPanel
      machineUrl={processStatus.machine}
      processId={processStatus.process_id}
      copilotParams={options}
    />
  )
}
