import {ProcessWithListLayout} from "../../../components/ProcessWithListLayout";
import {getApp} from "@/utils/eidolon-apps";

interface ChatbotLayoutProps {
  children: JSX.Element
}

export default function ChatbotLayout({children}: ChatbotLayoutProps) {
  const app = getApp('venture-agent')!
  return (
    <ProcessWithListLayout
      app={app}
    >
      {children}
    </ProcessWithListLayout>
  )
}
