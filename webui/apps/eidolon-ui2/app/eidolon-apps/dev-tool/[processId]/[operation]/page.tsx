'use client'

import {EidolonChatPanel} from "@/components/eidolon-chat-panel.tsx";

export interface ProcessPageProps {
  params: {
    processId: string
    operation?: string
  }
}

export default function ({params}: ProcessPageProps) {
  return <EidolonChatPanel app_name={"dev-tool"} processId={params.processId} operation={params.operation}/>
}
