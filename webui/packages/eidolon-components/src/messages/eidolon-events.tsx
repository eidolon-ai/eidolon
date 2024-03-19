'use client'

import {Box} from "@mui/material";
import {ElementsAndLookup} from "../lib/display-elements";
import "./eidolon-events.css"
import {ChatScrollAnchor} from "./chat-scroll-anchor";
import {ChatDisplayElement} from "./chat-display-element";
import {OperationInfo} from "@eidolon/client";

export interface EidolonEventProps {
  agentName: string,
  // eslint-disable-next-line no-unused-vars
  handleAction: (operation: OperationInfo, data: Record<string, any>) => void
  elementsAndLookup: ElementsAndLookup
}

export function EidolonEvents({elementsAndLookup, agentName, handleAction}: EidolonEventProps) {
  return (
    <Box id="chat-elements-scroll-region"
         sx={{overflowY: 'auto', overflowX: 'hidden', width: '60vw', marginBottom: '8px'}}>
      {elementsAndLookup.elements.map((child, index) => {
          if (index < elementsAndLookup.elements.length - 1 || child.type != "success") {
            return <ChatDisplayElement key={index} rawElement={child}
                                       topLevel={index == elementsAndLookup.elements.length - 1}
                                       agentName={agentName} handleAction={handleAction}/>
          }
        }
      )}
      <ChatScrollAnchor trackVisibility={true}></ChatScrollAnchor>
    </Box>
  )
}
