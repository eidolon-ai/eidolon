'use client'

import * as React from "react";
import {useEffect} from "react";
import {CopilotPanel, CopilotParams, EidolonApp, getOperations, getProcessStatus} from "@eidolon/components";
import {getApps} from "@/utils/app-registry-helper";

export interface ProcessPageProps {
  params: {
    app_name: string
    processId: string
  }
}

export default function ({params}: ProcessPageProps) {
  const [app, setApp] = React.useState<EidolonApp | undefined>(undefined)
  const [error, setError] = React.useState<string | undefined>(undefined)
  useEffect(() => {
    getApps().then((apps) => {
      const app = apps[params.app_name]
      if (!app) {
        setError("App not found")
      } else {
        const machineUrl = app.location!
        return getProcessStatus(machineUrl, params.processId).then((processStatus) => {
          return {processStatus, app}
        })
      }
    })
      .then((resp) => {
        const {processStatus, app} = resp!
        if (!processStatus) {
          setError("Process not found")
        } else {
          return getOperations(processStatus.machine, processStatus.agent).then((operations) => {
            return {operations, app}
          })
        }
      })
      .then((res) => {
        const {operations, app} = res!
        const options = app.params as CopilotParams
        const operation = operations.find((o) => o.name === options.operation)
        if (!operation) {
          setError("Operation not found")
        } else {
          options.operationInfo = operation
          if (operation.schema?.properties?.execute_on_cpu) {
            const property = operation.schema?.properties?.execute_on_cpu as Record<string, any>
            options.supportedLLMs = property?.["enum"] as string[]
            options.defaultLLM = property?.default as string
          }
          setApp(app)
        }
      })
      .catch((e) => {
        setError(e.message)
      })
  }, [params.app_name, params.processId]);

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
