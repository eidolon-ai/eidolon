'use client'

import {ElementsAndLookup} from "../lib/display-elements.ts";
import {ChatScrollAnchor} from "./chat-scroll-anchor.tsx";
import {ChatDisplayElement} from "./chat-display-element.tsx";

export interface EidolonEventProps {
  machineUrl: string
  agentName: string,
  elementsAndLookup: ElementsAndLookup,
  userImage: string | null | undefined
  userName: string | null  | undefined
  scrollableRegionRef?: React.RefObject<HTMLDivElement>
}

export function EidolonEvents({machineUrl, elementsAndLookup, agentName, userImage, userName, scrollableRegionRef}: EidolonEventProps) {
  return (
    <div id="chat-elements-scroll-region"
         ref={scrollableRegionRef}
         className={"flex flex-col gap-4 chat-elements-scroll-region overflow-y-auto overflow-x-hidden w-full mb-8"}
    >
      {elementsAndLookup.elements.map((child, index) => {
          if (index < elementsAndLookup.elements.length - 1 || child.type != "success") {
            return <ChatDisplayElement machineUrl={machineUrl} key={index} rawElement={child}
                                       topLevel={true}
                                       agentName={agentName}
                                       userImage={userImage}
                                       userName={userName}
            />
          }
        }
      )}
      <ChatScrollAnchor trackVisibility={true}></ChatScrollAnchor>
    </div>
  )
}
