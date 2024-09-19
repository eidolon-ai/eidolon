'use client'

import {getApp} from "@/utils/eidolon-apps";
import {EidolonApp, ProcessProvider} from "@eidolon-ai/components/client";
import {useEffect, useState} from "react";
import {MainAppLayout} from "@/layout/main-app-layout.tsx";

interface DevToolLayoutProps {
  children: JSX.Element
}

export default function DevToolLayout({children}: DevToolLayoutProps) {
  const [app, setApp] = useState<EidolonApp | undefined>(undefined)

  useEffect(() => {
    getApp('dev-tool').then(setApp)
  }, []);

  return (
    <>
      {app && (
        <MainAppLayout app={app}>
          <ProcessProvider>
            {children}
          </ProcessProvider>
        </MainAppLayout>
      )}
    </>
  )
}
