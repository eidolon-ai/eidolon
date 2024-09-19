import {createContext, ReactNode, useContext, useState} from "react";
import {getProcessStatus} from "../client-api-helpers/process-helper.ts";
import {HttpException, ProcessStatus} from "@eidolon-ai/client";
import {getApps, getOperations} from "../client-api-helpers/machine-helper.ts";
import {CopilotParams, DevParams, EidolonApp} from "../lib/util.ts";

interface ContextObject {
  processStatus?: ProcessStatus;
  app?: EidolonApp;
  fetchError?: HttpException;
  updateProcessStatus: (appName: string, processId: string) => Promise<void>;
}

const EidolonProcessContext = createContext<ContextObject | undefined>(undefined);

export const useProcess = (): ContextObject => {
  const context = useContext(EidolonProcessContext);
  if (!context) {
    throw new Error("useProcess must be used within a ProcessProvider");
  }
  return context;
};

interface ProcessProviderProps {
  children: ReactNode;
}

export const ProcessProvider: React.FC<ProcessProviderProps> = ({ children }) => {
  const [state, setState] = useState<Omit<ContextObject, 'updateProcessStatus'>>({});

  const updateProcessStatus = async (appName: string, processId: string): Promise<void> => {
    try {
      const apps = await getApps();
      const app = apps[appName];

      if (!app) {
        setState({fetchError: new HttpException(`App ${appName} not found`, 404)});
        return
      }

      const processStatus = await getProcessStatus(app.location, processId);

      if (app.type === "copilot") {
        const operations = await getOperations(processStatus.machine, processStatus.agent);
        const options = app.params as CopilotParams;
        const operation = operations.find((o) => o.name === options.operation);

        if (operation) {
          options.operationInfo = operation;
          if (operation.schema?.properties?.execute_on_apu) {
            const property = operation.schema.properties.execute_on_apu as Record<string, any>;
            options.supportedLLMs = property?.["enum"] as string[];
            options.defaultLLM = property?.default as string;
          }
        }
      } else {
        const options = app.params as DevParams;
        options.operations = await getOperations(processStatus.machine, processStatus.agent);
      }

      setState({ app, processStatus });
    } catch (error) {
      setState({ fetchError: error instanceof HttpException ? error : new HttpException('An unknown error occurred', 500) });
    }
  };

  const contextValue: ContextObject = {
    ...state,
    updateProcessStatus
  };

  return (
    <EidolonProcessContext.Provider value={contextValue}>
      {children}
    </EidolonProcessContext.Provider>
  );
};
