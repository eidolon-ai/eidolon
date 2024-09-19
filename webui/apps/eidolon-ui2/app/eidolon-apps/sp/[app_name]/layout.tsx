'use client'

import {getApp} from "@/utils/eidolon-apps";
import {EidolonApp, ProcessProvider} from "@eidolon-ai/components/client";
import {useEffect, useState} from "react";
import {MainAppLayout} from "@/layout/main-app-layout.tsx";

interface ChatbotLayoutProps {
  params: {
    app_name: string
  }
  children: JSX.Element
}

export default function ChatbotLayout({children}: ChatbotLayoutProps) {
  const [app, setApp] = useState<EidolonApp | undefined>(undefined)

  useEffect(() => {
    getApp('dev-tool').then(setApp)
  }, []);

  return (
    <MainAppLayout app={app}>
      <ProcessProvider>
        {children}
      </ProcessProvider>
    </MainAppLayout>
  )
}
