'use client'

import {getAppPathFromPath, ProcessList} from "@eidolon/components";
import {usePathname, useRouter} from "next/navigation";
import {ProcessStatus} from "@eidolon/client";

export interface DevProcessListProps {
  machineURL: string
}

export const DevProcessList = ({machineURL}: DevProcessListProps) => {
  const router = useRouter()
  const pathname = usePathname()

  return (
    <ProcessList
      machineURL={machineURL}
      isSelected={(process: ProcessStatus) => pathname.includes(process.process_id)}
      selectChat={(process: ProcessStatus) => {
        const appPath = getAppPathFromPath(pathname)
        if (appPath) {
          router.push(appPath  + `/${process.process_id}`)
        }
      }}
      goHome={() => {
      }}
    />
  )
}
