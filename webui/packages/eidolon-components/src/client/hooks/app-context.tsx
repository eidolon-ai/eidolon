import { createContext, ReactNode, useContext, useState, useEffect, useMemo } from "react";
import { HttpException } from "@eidolon-ai/client";
import { getApps, getOperations } from "../client-api-helpers/machine-helper.ts";
import { CopilotParams, DevParams, EidolonApp } from "../lib/util.ts";

interface AppContextObject {
  app?: EidolonApp;
  error?: HttpException;
  isLoading: boolean;
}

const EidolonAppContext = createContext<AppContextObject | undefined>(undefined);

const useFetchApp = (appName: string): AppContextObject => {
  const [app, setApp] = useState<EidolonApp | undefined>();
  const [error, setError] = useState<HttpException | undefined>();
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchApp = async () => {
      setIsLoading(true);
      try {
        const apps = await getApps();
        const selectedApp = apps[appName];

        if (!selectedApp) {
          throw new HttpException(`App ${appName} not found`, 404);
        }

        if (selectedApp.type === "copilot") {
          const options = selectedApp.params as CopilotParams;
          const operations = await getOperations(selectedApp.location, options.agent);
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
          const options = selectedApp.params as DevParams;
          options.operations = await getOperations(selectedApp.location, options.agent);
        }


        setApp(selectedApp);  // This line was missing in the original code
        setError(undefined);
      } catch (error) {
        setApp(undefined);
        setError(error instanceof HttpException ? error : new HttpException('An unknown error occurred', 500));
      } finally {
        setIsLoading(false);
      }
    };

    fetchApp();
  }, [appName]);

  return { app, error, isLoading };
};

export const useApp = (): AppContextObject => {
  const context = useContext(EidolonAppContext);
  if (!context) {
    throw new Error("useApp must be used within an AppProvider");
  }
  return context;
};

interface AppProviderProps {
  appName: string;
  children: ReactNode;
}

export const AppProvider: React.FC<AppProviderProps> = ({ appName, children }) => {
  const appData = useFetchApp(appName);

  return (
    <EidolonAppContext.Provider value={appData}>
      {children}
    </EidolonAppContext.Provider>
  );
};