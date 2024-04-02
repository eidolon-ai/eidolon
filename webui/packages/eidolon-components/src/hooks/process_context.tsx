'use client'

import {createContext, useContext, useState} from "react";
import {groupProcessesByUpdateDate} from "../process-list/group-processes";
import {getRootProcesses} from "../client-api-helpers/process-helper";
import {ProcessStatus} from "@eidolon/client";

const EidolonProcessesContext = createContext<{
  processes: Record<string, ProcessStatus[]>
  // eslint-disable-next-line no-unused-vars
  updateProcesses: (machineURL: string) => Promise<void>;
}>({
  processes: {},
  // eslint-disable-next-line no-unused-vars
  updateProcesses: async (machineURL: string) => {
  },
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

  const value = {
    processes: processesByDate,
    updateProcesses: async (machineURL: string) => {
      getRootProcesses(machineURL)
        .then(groupProcessesByUpdateDate)
        .then((chats) => {
          setProcessesByDate({...chats});
        });
    }
  };

  return (<EidolonProcessesContext.Provider value={value}>{children}</EidolonProcessesContext.Provider>)
}
