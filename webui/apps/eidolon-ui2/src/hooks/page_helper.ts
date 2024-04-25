import {useEffect} from "react";
import {getApps} from "../utils/app-registry-helper";
import {CopilotParams, EidolonApp, getOperations, getProcessStatus} from "@eidolon/components";
import * as React from "react";

export const useOperation = (app_name: string, processId: string) => {
  const [app, setApp] = React.useState<EidolonApp | undefined>(undefined)
  const [error, setError] = React.useState<string | undefined>(undefined)
  const [processStatus, setProcessStatus] = React.useState<any | undefined>(undefined)

  useEffect(() => {
    getApps().then((apps) => {
      const app = apps[app_name]
      if (!app) {
        setError("App not found")
      } else {
        const machineUrl = app.location!
        return getProcessStatus(machineUrl, processId).then((processStatus) => {
          return {processStatus, app}
        })
      }
    })
      .then((resp) => {
        const {processStatus, app} = resp!
        if (!processStatus) {
          setError("Process not found")
        } else {
          setProcessStatus(processStatus)
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
  }, [app_name, processId]);

  return {
    app,
    error,
    processStatus
  }
}