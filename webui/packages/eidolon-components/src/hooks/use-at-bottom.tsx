import {useEffect, useState} from "react";

export function useAtBottom() {
  const [isAtBottom, setIsAtBottom] = useState(false)
  const element = () => {
    return document.getElementById("chat-elements-scroll-region")!
  }
  useEffect(() => {
    const handleScroll = () => {
      if (element()) {
        const div = element()
        setIsAtBottom(div.scrollHeight - div.scrollTop - 1 < div.clientHeight)
      }
    }

    element()?.addEventListener('scroll', handleScroll, {passive: true})
    handleScroll()

    return () => {
      element()?.removeEventListener('scroll', handleScroll)
    }
  }, [])

  return isAtBottom
}
