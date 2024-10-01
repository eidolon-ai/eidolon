'use client'

import {createContext, useContext, useState} from "react";
import {groupProcessesByUpdateDate} from "../process-list/group-processes.ts";
import {getRootProcesses} from "../client-api-helpers/process-helper.ts";
import {HttpException, ProcessStatus} from "@eidolon-ai/client";

const EidolonProcessesContext = createContext<{
  processes: Record<string, ProcessStatus[]>
  updateProcesses: (machineURL: string) => Promise<void>;
  fetchError?: HttpException
}>({
  processes: {},
  updateProcesses: async (machineURL: string) => {
  },
  fetchError: undefined
});

// Custom hook to consume the context
export const useProcesses = () => {
  const context = useContext(EidolonProcessesContext);
  if (!context) {
    throw new Error("useProcessesContext must be used within a ProcessesProvider");
  }
  return context;
};

// Provider component
export const ProcessesProvider = ({children}: {children: JSX.Element}) => {
  const [processesByDate, setProcessesByDate] = useState<Record<string, ProcessStatus[]>>({})
  const [fetchError, setFetchError] = useState<HttpException | undefined>(undefined)
  const [loading, setLoading] = useState<boolean>(false)

  const value = {
    processes: processesByDate,
    fetchError: fetchError,
    updateProcesses: async (machineURL: string) => {
      if (!loading) {
        setLoading(true)
        getRootProcesses(machineURL)
          .then(groupProcessesByUpdateDate)
          .then((chats) => {
            setProcessesByDate({...chats});
            setFetchError(undefined)
            setLoading(false)
          }).catch((e) => {
          setProcessesByDate({chats: []})
          if (e instanceof HttpException) {
            setFetchError(e)
          } else {
            setFetchError(new HttpException(e.message || "unknown error", 500))
          }
          setLoading(false)
        })
      }
    }
  };

  return (<EidolonProcessesContext.Provider value={value}>{children}</EidolonProcessesContext.Provider>)
}
