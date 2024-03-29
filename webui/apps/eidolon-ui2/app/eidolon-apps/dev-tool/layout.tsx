import {ProcessWithListLayout} from "../../../components/ProcessWithListLayout"
import {PropsWithChildren} from "react";

interface DevToolLayoutProps {
  children: JSX.Element
}

export default function DevToolLayout({children}: DevToolLayoutProps) {
  return (
    <ProcessWithListLayout>
      {children}
    </ProcessWithListLayout>
  )
}
