'use client'

import {Box} from "@mui/material";
import {ElementsAndLookup} from "../lib/display-elements";
import "./eidolon-events.css"
import {ChatScrollAnchor} from "./chat-scroll-anchor";
import {ChatDisplayElement} from "./chat-display-element";

export interface EidolonEventProps {
  machineUrl: string
  agentName: string,
  elementsAndLookup: ElementsAndLookup,
  sx?: Record<any, any>
}

export function EidolonEvents({machineUrl, elementsAndLookup, agentName, ...props}: EidolonEventProps) {
  return (
    <Box id="chat-elements-scroll-region"
         sx={{overflowY: 'auto', overflowX: 'hidden', width: '60vw', marginBottom: '8px', ...props.sx}}
    >
      {elementsAndLookup.elements.map((child, index) => {
          if (index < elementsAndLookup.elements.length - 1 || child.type != "success") {
            return <ChatDisplayElement machineUrl={machineUrl} key={index} rawElement={child}
                                       topLevel={index == elementsAndLookup.elements.length - 1}
                                       agentName={agentName}/>
          }
        }
      )}
      <ChatScrollAnchor trackVisibility={true}></ChatScrollAnchor>
    </Box>
  )
}
