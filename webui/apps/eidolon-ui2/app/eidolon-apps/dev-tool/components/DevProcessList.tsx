'use client'

import {ProcessList} from "@eidolon/components";
import {usePathname, useRouter} from "next/navigation";
import {ProcessStatus} from "@eidolon/client";

export const DevProcessList = () => {
  const router = useRouter()
  const pathname = usePathname()

  return (
    <ProcessList
      isSelected={(process: ProcessStatus) => pathname.includes(process.process_id)}
      selectChat={(process: ProcessStatus) => {
        const pathSegments = pathname.split('/');
        const appNameIndex = pathSegments.findIndex((segment) => segment === 'eidolon-apps');

        if (appNameIndex !== -1 && appNameIndex + 1 < pathSegments.length) {
          const newPath = pathSegments.slice(0, appNameIndex + 2).join('/') + `/${process.process_id}`;
          router.push(newPath);
        }
      }}
      goHome={() => {
      }}
    />
  )
}
