'use client'

import * as React from 'react'
import {ButtonProps, Fab} from "@mui/material";
import ArrowDownwardIcon from "@mui/icons-material/ArrowDownward";
import {useEffect} from "react";
import {useAtBottom} from "@/lib/hooks/use-at-bottom";

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
        <ArrowDownwardIcon style={{fontSize: 36}}/>
      </Fab>
    )
  } else {
    return (
      <div/>
    )
  }
}
