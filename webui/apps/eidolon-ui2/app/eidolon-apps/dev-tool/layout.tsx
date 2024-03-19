import {ProcessWithListLayout} from "../../../components/ProcessWithListLayout"
import {PropsWithChildren} from "react";

export default function ChatbotLayout({children}: PropsWithChildren) {
  return (
    <ProcessWithListLayout>
      {children}
    </ProcessWithListLayout>
  )
}
