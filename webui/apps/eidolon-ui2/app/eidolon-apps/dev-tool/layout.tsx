import {ProcessWithListLayout} from "../../../components/ProcessWithListLayout"
import {getApp} from "@/utils/eidolon-apps";
import {ProcessProvider} from "@eidolon-ai/components/client";

interface DevToolLayoutProps {
  children: JSX.Element
}

export default function DevToolLayout({children}: DevToolLayoutProps) {
  const app = getApp('dev-tool')!
  return (
    <ProcessWithListLayout app={app}>
      <ProcessProvider>
        {children}
      </ProcessProvider>
    </ProcessWithListLayout>
  )
}
