'use client'

import {Box} from "@mui/material";
import {ElementsAndLookup} from "../lib/display-elements.ts";
import {ChatScrollAnchor} from "./chat-scroll-anchor.tsx";
import {ChatDisplayElement} from "./chat-display-element.tsx";

export interface EidolonEventProps {
  machineUrl: string
  agentName: string,
  elementsAndLookup: ElementsAndLookup,
  userImage: string | null | undefined
  userName: string | null  | undefined
  sx?: Record<any, any>
}

export function EidolonEvents({machineUrl, elementsAndLookup, agentName, userImage, userName, ...props}: EidolonEventProps) {
  return (
    <Box id="chat-elements-scroll-region"
         sx={{overflowY: 'auto', overflowX: 'hidden', width: '100%', marginBottom: '8px', ...props.sx}}
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
    </Box>
  )
}
