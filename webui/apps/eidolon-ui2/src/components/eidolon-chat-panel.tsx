'use client'

import {useEffect, useRef, useState} from "react";
import {CopilotPanel, getProcessStatus, useProcess} from "@eidolon-ai/components/client";
import {useSession} from "next-auth/react";
import { MessageSquare } from 'lucide-react'
import {useHeader} from "@/layout/HeaderContext.tsx";
import {ProcessStatus} from "@eidolon-ai/client";

export interface EidolonChatPanelProps {
  app_name: string
  processId: string
  operation?: string
}

interface BreadCrumb {
  title: string
  processId: string
}

export function EidolonChatPanel({app_name, processId, operation}: EidolonChatPanelProps) {
  const {app, fetchError, processStatus, updateProcessStatus} = useProcess()
  const {data: session} = useSession()
  const outerContainerRef = useRef<HTMLDivElement>(null);
  const innerContainerRef = useRef<HTMLDivElement>(null);
  const scrollableRegionRef = useRef<HTMLDivElement>(null);
  const [breadcrumbs, setBreadcrumbs] = useState<BreadCrumb[]>([])
  const { setHeaderCenter } = useHeader()

  useEffect(() => {
    setHeaderCenter((
      <div className={"mx-4 eidolon-handle-mouse-event flex flex-row justify-center items-center w-full flex-nowrap"}>
        <span className={"flex flex-row text-center"}><MessageSquare/></span>
        <div className={"flex flex-row text-center m-2 text-gray-500 text-nowrap"}>
          {breadcrumbs.map((b, i) => (
            <div key={i} className={"flex flex-row"}>
              {i > 0 && <span className={"mx-2"}>/</span>}
              <a href={b.processId}>{b.title}</a>
            </div>
          ))}
        </div>
      </div>
    ))
    return () => setHeaderCenter(null) // Cleanup
  }, [setHeaderCenter, breadcrumbs])

  useEffect(() => {
    const outerContainer = outerContainerRef.current!;

    const handleWheel = (event: WheelEvent) => {
      if (!outerContainerRef.current || !outerContainerRef.current || !innerContainerRef.current || !scrollableRegionRef.current) return;

      const { clientX } = event;
      const smallerDivRect = innerContainerRef.current.getBoundingClientRect();

      // Check if the scroll event occurred outside the smaller width div
      if (clientX < smallerDivRect.left || clientX > smallerDivRect.right) {
        // Prevent the default scroll on the outer container
        event.preventDefault();

        // Calculate the amount to scroll
        const scrollAmount = event.deltaY;

        // Apply the scroll to the chat panel
        scrollableRegionRef.current.scrollTop += scrollAmount;
      }
     };

    outerContainer.addEventListener('wheel', handleWheel, {passive: false});

    return () => {
      outerContainer.removeEventListener('wheel', handleWheel);
    };
  });

  useEffect(() => {
    updateProcessStatus(app_name, processId).then((ps: ProcessStatus) => {
      return ps
    })
  }, [processStatus?.state]);

  useEffect(() => {
    if (processStatus) {
      const breadcrumbs = [{title: processStatus.title || processStatus.agent || "unknown", processId: processStatus.process_id}]
      let current = processStatus.parent_process_id
      while (current) {
        const parent = getProcessStatus(processStatus.machine, current)
        breadcrumbs.unshift({title: parent.title || parent.agent || "New Chat", processId: current})
        current = parent.parent_process_id
      }
      setBreadcrumbs(breadcrumbs)
    }
  }, [processStatus?.parent_process_id, processStatus?.title]);

  return (
    <div
      ref={outerContainerRef}
      className={"flex flex-col items-center w-full h-full "}
    >
      <div className={"w-[65vw] overflow-hidden h-full"}>
        {!fetchError && !app && (<div>Loading...</div>)}
        {fetchError && (<div>{fetchError.message}</div>)}
        {app && !fetchError && (
          <CopilotPanel
            operation={operation}
            scrollableRegionRef={scrollableRegionRef}
            machineUrl={app!.location}
            processId={processId}
            copilotParams={app!.params}
            userName={session?.user?.name}
            userImage={session?.user?.image}
          />
        )}
      </div>
    </div>
  )
}
