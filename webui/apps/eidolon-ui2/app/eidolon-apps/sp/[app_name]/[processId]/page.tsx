'use client'

import * as React from "react";
import {CopilotPanel, CopilotParams, useProcess} from "@eidolon/components";

export interface ProcessPageProps {
  params: {
    app_name: string
    processId: string
  }
}

export default function ({params}: ProcessPageProps) {
  const {app, fetchError} = useProcess()

  if (!fetchError && !app) {
    return <div>Loading...</div>
  }
  if (fetchError) {
    return <div>{fetchError.message}</div>
  }
  return (
    <CopilotPanel
      machineUrl={app!.location}
      processId={params.processId}
      copilotParams={app!.params as CopilotParams}
    />
  )
}
