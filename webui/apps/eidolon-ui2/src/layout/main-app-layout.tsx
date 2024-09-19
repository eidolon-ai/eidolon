'use client'

import {EidolonApp, ProcessesProvider} from "@eidolon-ai/components/client";
import {DrawerSidebar} from "@/components/drawer-sidebar.tsx";
import {ProcessListPanel} from "../components/process-list-panel.tsx";


export interface DevTooLayoutProps {
  app: EidolonApp
  children: JSX.Element
}

export function MainAppLayout({children, app}: DevTooLayoutProps) {
  return (
    <ProcessesProvider>
      <div className={"flex flex-row h-full relative"}>
        <DrawerSidebar>
          <ProcessListPanel app={app}/>
        </DrawerSidebar>
        <div className={"flex flex-col justify-center max-w-full h-full w-full"} >
          {children}
        </div>
      </div>
    </ProcessesProvider>
  );
}
