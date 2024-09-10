'use client'

import * as React from "react";
import {useEffect} from "react";
import {DevPanel, DevParams, EidolonApp, getApps, getOperations, getProcessStatus} from "@eidolon-ai/components/client";
import {ProcessStatus} from "@eidolon-ai/client";

export interface ProcessPageProps {
  params: {
    processId: string
  }
}

export default function ({params}: ProcessPageProps) {
  const app_name = "dev-tool"
  const [app, setApp] = React.useState<EidolonApp | undefined>(undefined)
  const [error, setError] = React.useState<string | undefined>(undefined)

  useEffect(() => {
    getApps().then((apps: Record<string, EidolonApp>) => {
      const app = apps[app_name]
      if (!app) {
        throw new Error("App not found")
      } else {
        const machineUrl = app.location!
        return getProcessStatus(machineUrl, params.processId).then((processStatus: ProcessStatus) => {
          return {processStatus, app}
        })
      }
    })
      .then((resp: any) => {
        const {processStatus, app} = resp!
        if (!processStatus) {
          throw new Error("Process not found")
        } else {
          app.params.agent = processStatus.agent
          return getOperations(processStatus.machine, processStatus.agent).then((operations: any) => {
            return {operations, app}
          })
        }
      })
      .then((res: any) => {
        const {operations, app} = res!
        const options = app.params as DevParams
        options.operations = operations
        setApp(app)
      })
      .catch((e: Error) => {
        setError(e.message)
      })
  }, [params.processId]);


  if (error) {
    return <div>{error}</div>
  }
  if (!app) {
    return <div>Loading...</div>
  }
  return (
    <DevPanel machineUrl={app?.location!} devParams={app?.params as DevParams} processId={params.processId}/>
  )
}
