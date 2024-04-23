import {notFound} from "next/navigation";
import {_processHandler} from "../../../api/eidolon/eidolon_helpers";
import * as React from "react";
import {MessagesWithAction} from "@eidolon/components";
import {getApp} from "@/utils/eidolon-apps";
import {EidolonClient} from "@eidolon/client";

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
  // todo, use global client here so that openapi calls are cached
  const client = new EidolonClient(app.location)
  const operations = await client.getOperations(processStatus.agent, processStatus?.available_actions)
  return (
    <MessagesWithAction operations={operations} machineUrl={processStatus.machine} agent={processStatus.agent} processId={processStatus.process_id}/>
  )
}
