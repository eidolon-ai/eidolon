'use client'

import {EidolonChatPanel} from "@/components/eidolon-chat-panel.tsx";
import {ProcessProvider} from "@eidolon-ai/components/client";

export interface ProcessPageProps {
  params: {
    processId: string
    operation?: string
  }
}

export default function ({params}: ProcessPageProps) {
  return (
    <ProcessProvider processId={params.processId}>
      <EidolonChatPanel operation={params.operation}/>
    </ProcessProvider>
  )
}
