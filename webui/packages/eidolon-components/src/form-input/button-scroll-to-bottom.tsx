'use client'

import * as React from 'react'
import {ButtonProps, Fab} from "@mui/material";
import {ArrowDownward} from "@mui/icons-material";
import {useAtBottom} from "../hooks/use-at-bottom.js";

interface ButtonScrollToBottomProps extends ButtonProps {
}

export function ButtonScrollToBottom({className, ...props}: ButtonScrollToBottomProps) {
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
      <div/>
    )
  }
}
