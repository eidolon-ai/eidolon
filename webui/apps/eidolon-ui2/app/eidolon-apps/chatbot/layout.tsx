import {ProcessWithListLayout} from "../../../components/ProcessWithListLayout"

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