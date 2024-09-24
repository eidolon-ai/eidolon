'use client'

import React, { useEffect, useState, useRef, useLayoutEffect } from "react";
import { ElementsAndLookup } from "../lib/display-elements.ts";
import { ChatDisplayElement } from "./chat-display-element.tsx";

export interface EidolonEventProps {
  agentName: string;
  elementsAndLookup: ElementsAndLookup;
  userImage: string | null | undefined;
  userName: string | null | undefined;
  scrollableRegionRef: React.RefObject<HTMLDivElement>;
  goToProcess: (processId: string) => void;
}

export function EidolonEvents({
  elementsAndLookup,
  agentName,
  userImage,
  userName,
  scrollableRegionRef,
  goToProcess,
}: EidolonEventProps) {
  const [showTopFade, setShowTopFade] = useState(false);
  const [showBottomFade, setShowBottomFade] = useState(false);
  const [autoScroll, setAutoScroll] = useState(true);
  const prevScrollHeightRef = useRef<number>(0);

  const scrollToBottom = () => {
    if (scrollableRegionRef.current) {
      scrollableRegionRef.current.scrollTop = scrollableRegionRef.current.scrollHeight;
    }
  };

  const handleScroll = () => {
    if (scrollableRegionRef.current) {
      const { scrollTop, scrollHeight, clientHeight } = scrollableRegionRef.current;
      const isAtBottom = scrollHeight - clientHeight - scrollTop < 1;

      setShowTopFade(scrollTop > 0);
      setShowBottomFade(!isAtBottom);
      setAutoScroll(isAtBottom);
    }
  };

  useEffect(() => {
    const scrollElement = scrollableRegionRef.current;
    if (scrollElement) {
      scrollElement.addEventListener('scroll', handleScroll);
      return () => scrollElement.removeEventListener('scroll', handleScroll);
    }
  }, []);

  // This effect runs after every render
  useLayoutEffect(() => {
    const scrollElement = scrollableRegionRef.current;
    if (scrollElement) {
      const currentScrollHeight = scrollElement.scrollHeight;

      if (currentScrollHeight > prevScrollHeightRef.current && autoScroll) {
        scrollToBottom();
      }

      prevScrollHeightRef.current = currentScrollHeight;
    }
  });

  return (
    <div className="relative flex overflow-hidden">
      <div
        id="chat-elements-scroll-region"
        ref={scrollableRegionRef}
        className="flex flex-col gap-4 chat-elements-scroll-region overflow-y-auto overflow-x-hidden w-full"
      >
        {elementsAndLookup.elements.map((child, index) => (
          <ChatDisplayElement
            key={index}
            rawElement={child}
            topLevel={true}
            agentName={agentName}
            userImage={userImage}
            userName={userName}
            depth={0}
            goToProcess={goToProcess}
          />
        ))}
      </div>
      {showTopFade && (
        <div className="absolute top-0 left-0 right-[14px] h-10 bg-gradient-to-b from-gray-100 to-transparent pointer-events-none" />
      )}
      {showBottomFade && (
        <div className="absolute bottom-0 left-0 right-[14px] h-10 bg-gradient-to-t from-gray-100 to-transparent pointer-events-none" />
      )}
    </div>
  );
}