'use client'

import {createContext, useContext, useState} from "react";
import {getProcessStatus} from "../client-api-helpers/process-helper";
import {HttpException, ProcessStatus} from "@eidolon/client";
import {getApps} from "../client-api-helpers/machine-helper";
import {EidolonApp} from "../lib/util";

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
  const [loading, setLoading] = useState<boolean>(false)

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
        processStatus: undefined,
        app: undefined,
        fetchError: undefined
      }
      if (!loading) {
        console.log("fetching")
        setLoading(true)
        const app = (await getApps())[appName]
        if (!app) {
          ret.fetchError = new HttpException(`App ${appName} not found`, 404)
        } else {
          ret.app = app
          ret.processStatus = await getProcessStatus(app.location, processId)
        }
        setProcessStatus(ret.processStatus)
        setApp(ret.app)
        setFetchError(ret.fetchError)
        setLoading(false)
      }

      return ret
    }
  }

  return (<EidolonProcessContext.Provider value={value}>{children}</EidolonProcessContext.Provider>)
}
