import {ProcessWithListLayout} from "../../../components/ProcessWithListLayout"
import {PropsWithChildren} from "react";
import {getApp} from "@/utils/eidolon-apps";

interface DevToolLayoutProps {
  children: JSX.Element
}

export default function DevToolLayout({children}: DevToolLayoutProps) {
  const app = getApp('dev-tool')!
  return (
    <ProcessWithListLayout app={app}>
      {children}
    </ProcessWithListLayout>
  )
}
