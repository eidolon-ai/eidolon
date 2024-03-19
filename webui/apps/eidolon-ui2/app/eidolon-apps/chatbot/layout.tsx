import {ProcessWithListLayout} from "../../../components/ProcessWithListLayout"
import {PropsWithChildren} from "react";

interface ChatbotLayoutProps {
  children: JSX.Element
}

export default function ChatbotLayout({children}: ChatbotLayoutProps) {
  return (
    <ProcessWithListLayout
      agentName={"conversational_agent"}
    >
      {children}
    </ProcessWithListLayout>
  )
}