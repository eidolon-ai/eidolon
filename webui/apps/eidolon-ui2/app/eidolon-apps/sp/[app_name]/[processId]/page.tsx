'use client'

import {EidolonChatPanel} from "@/components/eidolon-chat-panel.tsx";
import {useNewChatOptions} from "../new-chat-options.tsx";
import {ProcessProvider} from "@eidolon-ai/components/client";

export interface ProcessPageProps {
  params: {
    app_name: string
    processId: string
  }
}

export default function ({params}: ProcessPageProps) {
  const {options, clearOptions} = useNewChatOptions()

  return (
    <ProcessProvider processId={params.processId}>
      <EidolonChatPanel options={options} clearOptions={clearOptions}/>
    </ProcessProvider>
  )
}
