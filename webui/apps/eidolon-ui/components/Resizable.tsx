'use client'

import * as React from "react";
import {useCallback, useEffect, useState} from "react";
import {cn} from "@/lib/utils";

interface ResizableOptions extends React.ComponentProps<'p'> {
  className: string
  targetComponentId: string
}

interface MouseEventFn {
  (evt: MouseEvent): void;
}

interface StartInfo {
  invert: boolean
  startClientX: number
}

export const Resizable = ({className, targetComponentId, ...props}: ResizableOptions) => {
  const [element, setElement] = useState<HTMLElement | null>(null)
  useEffect(() => {
    let elementById = document.getElementById(targetComponentId) as HTMLElement;
    setElement(elementById)
  }, [targetComponentId])

  const setSize = useCallback((newSize: number) => {
    if (element)
      element.style.width = `${newSize}px`
  }, [element])

  const getSize = useCallback(() => element?.style?.width || "0", [element])

  const [startInfo, setStartInfo] = useState<StartInfo | null>(null)

  const stopResizing = React.useCallback<MouseEventFn>(() => {
    if (startInfo && element) {
      localStorage.setItem(`${targetComponentId}-storage`, getSize())
      setStartInfo(null)
    }
  }, [element, getSize, startInfo, targetComponentId])

  const resize = React.useCallback<MouseEventFn>((mouseMoveEvent) => {
    if (startInfo) {
      let newWidth = mouseMoveEvent.clientX - (element?.getBoundingClientRect()?.left || 0)
      if (startInfo.invert) {
        newWidth = (element?.getBoundingClientRect()?.right || 0) - mouseMoveEvent.clientX
      }
      // console.log("current", element().getBoundingClientRect().width, "to", mouseMoveEvent.clientX, "newWidth", newWidth, startInfo.invert)
      setSize(newWidth)
    }
  }, [element, startInfo, setSize])

  React.useEffect(() => {
    if (document.getElementById(targetComponentId)) {
      setSize(parseInt(localStorage.getItem(`${targetComponentId}-storage`) || "150"))
    }
    window.addEventListener("mousemove", resize as EventListener)
    window.addEventListener("mouseup", stopResizing)
    return () => {
      window.removeEventListener("mousemove", resize)
      window.removeEventListener("mouseup", stopResizing)
    }
  }, [resize, setSize, stopResizing, targetComponentId])

  return (
    <div
      className={cn("bg-border hover:bg-gray-300", className)}
      {...props}
      onMouseDown={(event) => {
        event.preventDefault()
        event.stopPropagation()
        setStartInfo({
          startClientX: event.clientX,
          invert: (element?.getBoundingClientRect()?.left || 0) > event.clientX
        } as StartInfo)
      }}
    ></div>
  );
};
