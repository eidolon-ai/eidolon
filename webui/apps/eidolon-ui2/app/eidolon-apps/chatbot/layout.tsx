import {ProcessWithListLayout} from "../../../components/ProcessWithListLayout"
import {PropsWithChildren} from "react";

export default function ChatbotLayout({children}: PropsWithChildren) {
  return (
    <ProcessWithListLayout
      agentName={"conversational_agent"}
    >
      {children}
    </ProcessWithListLayout>
  )
}