'use client'

import * as React from "react";
import {ProcessProvider} from "@eidolon/components/client";
import PageWithStepper from "./PageWithStepper";

interface ChatbotLayoutProps {
  children: JSX.Element
  params: {
    processId: string
  }
}

export default function ChatbotLayout({children, params}: ChatbotLayoutProps) {
  return (
    <ProcessProvider>
      <PageWithStepper params={params} children={children}/>
    </ProcessProvider>
  )
}
