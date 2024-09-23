'use client'

import {useEffect, useRef} from "react";
import {MainAppLayout} from "@/layout/main-app-layout.tsx";
import {NewChatOptionsProvider, useNewChatOptions} from "./new-chat-options.tsx";

interface LayoutProps {
  children: JSX.Element
  params: {
    app_name: string
  }
}


export default function DevToolLayout({children, params}: LayoutProps) {
  return (
    <MainAppLayout app_name={params.app_name}>
      <NewChatOptionsProvider>
        {children}
      </NewChatOptionsProvider>
    </MainAppLayout>
  )
}
