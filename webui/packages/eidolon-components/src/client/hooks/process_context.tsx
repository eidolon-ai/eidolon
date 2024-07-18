'use client'

import {createContext, useContext, useState} from "react";
import {getProcessStatus} from "../client-api-helpers/process-helper.ts";
import {HttpException, ProcessStatus} from "@eidolon/client";
import {getApps, getOperations} from "../client-api-helpers/machine-helper.ts";
import {CopilotParams, EidolonApp} from "../lib/util.ts";

export interface ContextObject {
  processStatus?: ProcessStatus
  app?: EidolonApp
  // eslint-disable-next-line no-unused-vars
  updateProcessStatus: (appName: string, processId: string) => Promise<{
    processStatus?: ProcessStatus,
    app?: EidolonApp,
    fetchError?: HttpException
  }>;
  fetchError?: HttpException
}

const EidolonProcessContext = createContext<ContextObject>({
  app: undefined,
  processStatus: undefined,
  // eslint-disable-next-line no-unused-vars
  updateProcessStatus: async (appName: string, processId: string) => {
    return {processStatus: undefined, app: undefined}
  },
  fetchError: undefined
});

// Custom hook to consume the context
export const useProcess = () => {
  const context = useContext(EidolonProcessContext);
  if (!context) {
    throw new Error("useProcessesContext must be used within a ProcessesProvider");
  }
  return context;
}

// Provider component
export const ProcessProvider = ({children}: { children: JSX.Element }) => {
  const [processStatus, setProcessStatus] = useState<ProcessStatus | undefined>(undefined)
  const [app, setApp] = useState<EidolonApp | undefined>(undefined)
  const [fetchError, setFetchError] = useState<HttpException | undefined>(undefined)

  const value = {
    app: app,
    processStatus: processStatus,
    fetchError: fetchError,
    updateProcessStatus: async (appName: string, processId: string) => {
      const ret: {
        processStatus?: ProcessStatus,
        app?: EidolonApp,
        fetchError?: HttpException
      } = {
        processStatus: processStatus,
        app: app,
        fetchError: fetchError
      }

      const innerApp = (await getApps())[appName]

      if (!innerApp) {
        ret.fetchError = new HttpException(`App ${appName} not found`, 404)
      } else {
        ret.app = innerApp
        ret.processStatus = await getProcessStatus(innerApp.location, processId)
        if (innerApp.type === "copilot") {
          const operations = await getOperations(ret.processStatus!.machine, ret.processStatus!.agent)
          const options = innerApp.params as CopilotParams
          const operation = operations.find((o) => o.name === options.operation)
          if (!operation) {
            ret.fetchError = new HttpException(`Operation ${options.operation} not found`, 404)
          } else {
            options.operationInfo = operation
            if (operation.schema?.properties?.execute_on_apu) {
              const property = operation.schema?.properties?.execute_on_apu as Record<string, any>
              options.supportedLLMs = property?.["enum"] as string[]
              options.defaultLLM = property?.default as string
            }
          }
        }
      }

      setProcessStatus(ret.processStatus)
      setApp(ret.app)
      setFetchError(ret.fetchError)
      return ret
    }
  }

  return (<EidolonProcessContext.Provider value={value}>{children}</EidolonProcessContext.Provider>)
}
