'use client'

import * as React from "react";
import {Box, LinearProgress} from "@mui/material";
import {executeOperation} from "@eidolon/components/src/client-api-helpers/process-event-helper";
import {CopilotParams, useProcess} from "@eidolon/components";
import StartProcessInputForm from "./StartProcessInputForm";
import {useRouter} from "next/navigation";

export interface ProcessPageProps {
  params: {
    processId: string
  }
}

export default function ({params}: ProcessPageProps) {
  const app_name = 'venture-agent'
  const {app, fetchError, processStatus, updateProcessStatus} = useProcess()
  const [executing, setExecuting] = React.useState<boolean>(false)
  const router = useRouter()

  const handleStartProcess = async (ventureSite: string) => {
    const appOptions = app!.params as CopilotParams

    setExecuting(true)
    executeOperation(app!.location, appOptions.agent, "find_companies", processStatus!.process_id, {
      venture_site: ventureSite,
    }).then(() => {
      setExecuting(false)
      router.push(`choose`)
    })
  }


  if (!fetchError && !app) {
    return <div></div>
  }
  if (fetchError) {
    return <div>{fetchError.message}</div>
  }
  return (
    <Box sx={{display: 'flex', justifyContent: 'center'}}>
      <Box sx={{width: "55vw", display: 'flex', flexDirection:"column"}}>
      {executing && (
        <Box sx={{width: "100%"}}>
          <LinearProgress/>
        </Box>
      )}
      <div style={{position: "relative", height: "fit-content"}}>
        <StartProcessInputForm handleStartProcess={handleStartProcess} loading={executing}/>
      </div>
      </Box>
    </Box>
  )
}
