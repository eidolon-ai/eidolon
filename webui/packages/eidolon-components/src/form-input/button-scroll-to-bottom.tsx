'use client'

import {Fab} from "@mui/material";
import {ArrowDownward} from "@mui/icons-material";
import {useAtBottom} from "../hooks/use-at-bottom";

export function ButtonScrollToBottom() {
  const isAtBottom = useAtBottom()

  if (!isAtBottom) {
    return (
      <Fab size={"small"}
           onClick={() => {
             const div = document.getElementById('chat-elements-scroll-region')
             if (div) {
               div.scrollTop = div.scrollHeight
             }
           }}
      >
        <ArrowDownward style={{fontSize: 36}}/>
      </Fab>
    )
  } else {
    return (
      <div style={{height: "32px"}}/>
    )
  }
}
