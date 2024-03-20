import {notFound} from "next/navigation";
import {_processHandler} from "../../../api/eidolon/eidolon_helpers";
import manifest from "../manifest.json";
import * as React from "react";
import {MessagesWithAction} from "@/components/MessagesWithAction";
import {MessagesWithSingleAction} from "@/components/MessagesWithSingleAction";

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
    <MessagesWithSingleAction
      machineUrl={processStatus.machine}
      agent={processStatus.agent}
      processId={processStatus.process_id}
      operationName={"converse"}
      inputLabel={"Enter question about the documentation here..."}
    />
  )
}
