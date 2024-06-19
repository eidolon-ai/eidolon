'use client'

import * as React from "react";
import {CopilotPanel, CopilotParams, useProcess} from "@eidolon/components/client";
import {Box} from "@mui/material";
import {useSession} from "next-auth/react";
import {useEffect} from "react";

export interface ProcessPageProps {
  params: {
    app_name: string
    processId: string
  }
}

export default function ({params}: ProcessPageProps) {
  const {app, fetchError, processStatus, updateProcessStatus} = useProcess()
  const {data: session} = useSession()

  useEffect(() => {
    updateProcessStatus(params.app_name, params.processId)
  }, [processStatus?.state]);

  if (!fetchError && !app) {
    return <div>Loading...</div>
  }
  if (fetchError) {
    return <div>{fetchError.message}</div>
  }
  return (
    <Box sx={{width: '65vw'}}>
      <CopilotPanel
        machineUrl={app!.location}
        processId={params.processId}
        copilotParams={app!.params as CopilotParams}
        userName={session?.user?.name}
        userImage={session?.user?.image}
      />
    </Box>
  )
}
