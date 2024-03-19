'use client'

import {useInView} from 'react-intersection-observer'

import {useAtBottom} from '../hooks/use-at-bottom'
import {useEffect} from "react";

interface ChatScrollAnchorProps {
  trackVisibility?: boolean
}

export function ChatScrollAnchor({trackVisibility}: ChatScrollAnchorProps) {
  const isAtBottom = useAtBottom()
  const {ref, entry, inView} = useInView({
    trackVisibility,
    delay: 100,
    rootMargin: '0px 0px -150px 0px'
  })

  useEffect(() => {
    if (isAtBottom && trackVisibility && !inView) {
      entry?.target.scrollIntoView({
        block: 'start'
      })
    }
  }, [inView, entry, isAtBottom, trackVisibility])

  return <div ref={ref} style={{width: "100%", height: "1px"}}/>
}
