'use client'

import {DevProcessListWithAdd} from "./ProcessListWithAdd";
import {EidolonApp, ProcessesProvider} from "@eidolon-ai/components/client";
import {useState} from "react";
import {DrawerSidebar} from "@/components/drawer-sidebar.tsx";


export interface DevTooLayoutProps {
  app: EidolonApp
  children: JSX.Element
}

export function ProcessWithListLayout({children, app}: DevTooLayoutProps) {
  const [width, setWidth] = useState(0)

  return (
    <ProcessesProvider>
      <div className={"flex flex-row h-full relative"}>
        <DrawerSidebar>
          <DevProcessListWithAdd app={app}/>
        </DrawerSidebar>
        <div className={"flex flex-col justify-center max-w-full h-full w-full"} >
          {children}
        </div>
      </div>
    </ProcessesProvider>
  );
}
