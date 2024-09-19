'use client'

import {EidolonChatPanel} from "@/components/eidolon-chat-panel.tsx";

export interface ProcessPageProps {
  params: {
    app_name: string
    processId: string
  }
}

export default function ({params}: ProcessPageProps) {
  return <EidolonChatPanel app_name={"dev-tool"} processId={params.processId} advanced_input={true}/>
}
