import {notFound} from "next/navigation";
import {_processHandler} from "../../../api/eidolon/eidolon_helpers";
import manifest from "../manifest.json";
import {MessagesWithAction} from "@eidolon/components";
import * as React from "react";

export interface ProcessPageProps {
  params: {
    processId: string
  }
}

export default async function ({params}: ProcessPageProps) {
  const processStatus = await _processHandler.getProcess(manifest.location, params.processId)
  if (!processStatus) {
    notFound()
  }

  return (
    <MessagesWithAction machineUrl={processStatus.machine} agent={processStatus.agent} processId={processStatus.process_id}/>
  )
}
