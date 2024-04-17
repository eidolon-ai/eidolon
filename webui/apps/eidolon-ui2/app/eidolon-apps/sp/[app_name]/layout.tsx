import {ProcessWithListLayout} from "../../../../components/ProcessWithListLayout";
import {getApp} from "@/utils/eidolon-apps";

interface ChatbotLayoutProps {
  params: {
    app_name: string
  }
  children: JSX.Element
}

export default function ChatbotLayout({children, params}: ChatbotLayoutProps) {
  const app = getApp(params.app_name)!
  return (
    <ProcessWithListLayout
      app={app}
    >
      {children}
    </ProcessWithListLayout>
  )
}