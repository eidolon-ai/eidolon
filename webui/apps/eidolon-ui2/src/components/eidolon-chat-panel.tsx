'use client'

import {useEffect, useRef, useState} from "react";
import {ConversationPanel, createProcess, getProcessStatus, useApp, useProcess, useProcesses} from "@eidolon-ai/components/client";
import {useSession} from "next-auth/react";
import {MessageSquare} from 'lucide-react'
import {useHeader} from "@/layout/HeaderContext.tsx";
import {ProcessStatus} from "@eidolon-ai/client";
import {useRouter} from "next/navigation";
import {NewChatOptions} from "../../app/eidolon-apps/sp/[app_name]/new-chat-options.tsx";

export interface EidolonChatPanelProps {
  operation?: string
  options?: NewChatOptions
  clearOptions?: () => void
}

interface BreadCrumb {
  title: string
  processId: string
}

export function EidolonChatPanel({operation, options, clearOptions}: EidolonChatPanelProps) {
  const {app} = useApp()
  const {fetchError, processStatus} = useProcess()
  const {updateProcesses} = useProcesses()
  const {data: session} = useSession()
  const outerContainerRef = useRef<HTMLDivElement>(null);
  const innerContainerRef = useRef<HTMLDivElement>(null);
  const scrollableRegionRef = useRef<HTMLDivElement>(null);
  const [breadcrumbs, setBreadcrumbs] = useState<BreadCrumb[]>([])
  const {setHeaderCenter} = useHeader()
  const router = useRouter()

  useEffect(() => {
    setHeaderCenter((
      <div className={"mx-4 eidolon-handle-mouse-event flex flex-row justify-center items-center w-full flex-nowrap overflow-hidden"}>
        <span className={"flex flex-row text-center"}><MessageSquare/></span>
        <div className={"flex flex-row text-center m-2 text-gray-500 text-nowrap"}>
          {breadcrumbs.map((b, i) => (
            <div key={i} className={"flex flex-row overflow-ellipsis text-ellipsis"}>
              {i > 0 && <span className={"mx-2"}>/</span>}
              <a href={b.processId}>{b.title}</a>
            </div>
          ))}
        </div>
      </div>
    ))
    return () => setHeaderCenter(null) // Cleanup
  }, [setHeaderCenter, breadcrumbs, processStatus?.title])

  useEffect(() => {
    const outerContainer = outerContainerRef.current!;

    const handleWheel = (event: WheelEvent) => {
      if (!outerContainerRef.current || !outerContainerRef.current || !innerContainerRef.current || !scrollableRegionRef.current) return;

      const {clientX} = event;
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
    async function loadBreadcrumb() {
      if (processStatus) {
        const breadcrumbs: BreadCrumb[] = [{title: processStatus.title || processStatus.agent || "unknown", processId: processStatus.process_id}]
        let current = processStatus.parent_process_id
        while (current) {
          const parent = await getProcessStatus(processStatus.machine, current)
          breadcrumbs.unshift({title: parent.title || parent.agent || "New Chat", processId: current})
          current = parent.parent_process_id
        }
        return breadcrumbs
      } else {
        return []
      }
    }
    loadBreadcrumb().then(bc => setBreadcrumbs(bc))
  }, [processStatus?.parent_process_id, processStatus?.title]);

  const handleNewConversation = () => {
    let title
    if (app.params.type === 'copilot') {
      title = app.params.newItemText || "New Chat"
    } else {
      title = `${processStatus?.agent}`
      if (operation) {
        title += `:${operation}`
      }
    }
    createProcess(app.location, processStatus?.agent, title).then((process: ProcessStatus | null) => {
      if (process) {
        router.push(`/eidolon-apps/${app.path}/${process.process_id}${operation ? '/' + operation : ''}`);
      }
    }).then(() => updateProcesses(app.location));
  }

  const goToProcess = (processId: string) => {
    console.log("goToProcess", processId)
    router.push(`/eidolon-apps/${app.path}/${processId}`);
  }

  return (
    <div
      ref={outerContainerRef}
      className={"flex flex-col items-center w-full h-full font-serif"}
    >
      <div className={"w-[65vw] overflow-hidden h-full"}>
        {!fetchError && !app && (<div>Loading...</div>)}
        {fetchError && (<div>{fetchError.message}</div>)}
        {app && !fetchError && (
          <ConversationPanel
            operation={operation}
            scrollableRegionRef={scrollableRegionRef}
            machineUrl={app!.location}
            agent={processStatus?.agent}
            processId={processStatus?.process_id}
            copilotParams={app!.params}
            userName={session?.user?.name}
            userImage={session?.user?.image}
            handleNewConversation={handleNewConversation}
            options={options}
            clearOptions={clearOptions || (() => {
            })}
            goToProcess={goToProcess}
          />
        )}
      </div>
    </div>
  )
}
