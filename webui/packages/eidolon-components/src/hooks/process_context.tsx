'use client'

import {createContext, useContext, useState} from "react";
import {getProcessStatus} from "../client-api-helpers/process-helper";
import {HttpException, ProcessStatus} from "@eidolon/client";

const EidolonProcessContext = createContext<{
  processStatus?: ProcessStatus
  // eslint-disable-next-line no-unused-vars
  updateProcessStatus: (machineURL: string, processId: string) => Promise<void>;
  fetchError?: HttpException
}>({
  processStatus: undefined,
  // eslint-disable-next-line no-unused-vars
  updateProcessStatus: async (machineURL: string, processId: string) => {
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
};

// Provider component
export const ProcessProvider = ({children}: {children: JSX.Element}) => {
  const [processStatus, setProcessStatus] = useState<ProcessStatus | undefined>(undefined)
  const [fetchError, setFetchError] = useState<HttpException | undefined>(undefined)

  const value = {
    processStatus: processStatus,
    fetchError: fetchError,
    updateProcessStatus: async (machineURL: string, processId: string) => {
      getProcessStatus(machineURL, processId).then((processStatus) => {
        setProcessStatus(processStatus)
        setFetchError(undefined)
        }).catch((e) => {
          setProcessStatus(undefined)
          if (e instanceof HttpException) {
            setFetchError(e)
          } else {
            setFetchError(new HttpException(e.message || "unknown error", 500))
          }
      })
    }
  };

  return (<EidolonProcessContext.Provider value={value}>{children}</EidolonProcessContext.Provider>)
}
