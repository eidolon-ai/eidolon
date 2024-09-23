'use client'

import {AppProvider, EidolonApp, ProcessesProvider} from "@eidolon-ai/components/client";
import {DrawerSidebar} from "@/components/drawer-sidebar.tsx";
import {ProcessListPanel} from "../components/process-list-panel.tsx";


export interface DevTooLayoutProps {
  app_name: string
  children: JSX.Element
}

export function MainAppLayout({children, app_name}: DevTooLayoutProps) {
  return (
    <ProcessesProvider>
      <AppProvider appName={app_name}>
        <div className={"flex flex-row h-full relative"}>
          <DrawerSidebar>
            <ProcessListPanel/>
          </DrawerSidebar>
          <div className={"flex flex-col justify-center max-w-full h-full w-full"}>
            {children}
          </div>
        </div>
      </AppProvider>
    </ProcessesProvider>
  );
}
