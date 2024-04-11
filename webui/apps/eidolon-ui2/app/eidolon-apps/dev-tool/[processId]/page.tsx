import {notFound} from "next/navigation";
import {_processHandler} from "../../../api/eidolon/eidolon_helpers";
import * as React from "react";
import {MessagesWithAction} from "@eidolon/components";
import {CopilotParams, getApp} from "@/utils/eidolon-apps";

export interface ProcessPageProps {
  params: {
    processId: string
  }
}

export default async function ({params}: ProcessPageProps) {
  let app = getApp("dev-tool")
  const processStatus = await _processHandler.getProcess(app.location, params.processId)
  if (!processStatus) {
    notFound()
  }

  return (
    <MessagesWithAction machineUrl={processStatus.machine} agent={processStatus.agent} processId={processStatus.process_id}/>
  )
}
