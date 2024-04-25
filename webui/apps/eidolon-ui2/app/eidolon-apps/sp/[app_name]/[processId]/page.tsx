'use client'

import * as React from "react";
import {CopilotPanel, CopilotParams} from "@eidolon/components";
import {useOperation} from "@/hooks/page_helper";

export interface ProcessPageProps {
  params: {
    app_name: string
    processId: string
  }
}

export default function ({params}: ProcessPageProps) {
  const {app, error} = useOperation(params.app_name, params.processId)

  if (!error && !app) {
    return <div>Loading...</div>
  }
  if (error) {
    return <div>{error}</div>
  }
  return (
    <CopilotPanel
      machineUrl={app!.location}
      processId={params.processId}
      copilotParams={app!.params as CopilotParams}
    />
  )
}
