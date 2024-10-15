import { createContext, ReactNode, useContext, useState, useEffect, useMemo, useCallback } from "react";
import { getProcessStatus } from "../client-api-helpers/process-helper.ts";
import { HttpException, ProcessStatus } from "@eidolon-ai/client";
import { useApp } from "./app-context.js";
import {useProcesses} from "./processes_context.js";

interface ContextObject {
  processStatus?: ProcessStatus;
  error?: HttpException;
  updateProcessStatus: () => Promise<void>;
}

const EidolonProcessContext = createContext<ContextObject | undefined>(undefined);

export const useProcess = () => {
  const context = useContext(EidolonProcessContext);
  if (!context) {
    throw new HttpException("useProcess must be used within a ProcessProvider", 500);
  }
  return context;
};

interface ProcessProviderProps {
  children: ReactNode;
  processId: string;
}

export const ProcessProvider: React.FC<ProcessProviderProps> = ({ children, processId }) => {
  const [processStatus, setProcessStatus] = useState<ProcessStatus | undefined>();
  const [error, setError] = useState<HttpException | undefined>();
  const { app } = useApp();
  const {updateProcesses} = useProcesses();

  const fetchProcessStatus = useCallback(async () => {
    if (app?.location) {
      try {
        const existingTitle = processStatus?.title;
        const status = await getProcessStatus(app.location, processId);
        setProcessStatus(status);
        if (status.title !== existingTitle) {
          await updateProcesses(app.location);
        }
        setError(undefined);
      } catch (error) {
        console.error('Error fetching process status:', error);
        setProcessStatus(undefined);
        setError(error instanceof HttpException ? error : new HttpException('An unknown error occurred', 500));
      }
    }
  }, [app?.location, processId]);

  useEffect(() => {
    fetchProcessStatus();
  }, [fetchProcessStatus]);

  const updateProcessStatus = useCallback(async (): Promise<void> => {
    await fetchProcessStatus();
  }, [fetchProcessStatus]);

  const contextValue = useMemo(() => ({
    processStatus,
    error,
    updateProcessStatus
  }), [processStatus, error, updateProcessStatus]);

  return (
    <EidolonProcessContext.Provider value={contextValue}>
      {children}
    </EidolonProcessContext.Provider>
  );
}