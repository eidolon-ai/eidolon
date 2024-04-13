import {notFound} from "next/navigation";
import * as React from "react";
import {getApp} from "@/utils/eidolon-apps";
import {_processHandler} from "../../../../api/eidolon/eidolon_helpers";
import {CopilotPanel, CopilotParams} from "@eidolon/components";
import {EidolonClient} from "@eidolon/client";

export interface ProcessPageProps {
  params: {
    app_name: string
    processId: string
  }
}

export default async function ({params}: ProcessPageProps) {
  let app = getApp(params.app_name)!
  if (!app) {
    notFound()
  }
  const options = app.params as CopilotParams
  const machineUrl = app.location!
  const processStatus = await _processHandler.getProcess(machineUrl, params.processId)
  if (!processStatus) {
    notFound()
  }

  const client = new EidolonClient(machineUrl)
  const action = await client.getAction(processStatus.agent, options.operation)
  if(!action) {
    throw new Error("No actions found")
  }

  let supportedLLMs: string[] = []
  if (action.schema?.properties?.execute_on_cpu) {
    const property = action.schema?.properties?.execute_on_cpu as Record<string, any>
    supportedLLMs = property?.["enum"] as string[]
  }
  return (
    <CopilotPanel
      supportedLLMs={supportedLLMs}
      operation={action}
      machineUrl={processStatus.machine}
      processId={processStatus.process_id}
      copilotParams={options}
    />
  )
}
