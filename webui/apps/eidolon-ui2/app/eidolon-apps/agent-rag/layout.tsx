import {ProcessWithListLayout} from "../../../components/ProcessWithListLayout"
import {PropsWithChildren} from "react";

interface ChatbotLayoutProps {
  children: JSX.Element
}

export default function ChatbotLayout({children}: ChatbotLayoutProps) {
  return (
    <ProcessWithListLayout
      agentName={"repo_expert"}
    >
      {children}
    </ProcessWithListLayout>
  )
}