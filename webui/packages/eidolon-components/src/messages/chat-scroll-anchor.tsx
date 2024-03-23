'use client'

import {useInView} from 'react-intersection-observer'

import {useEffect} from "react";
import {useAtBottom} from '../hooks/use-at-bottom'

interface ChatScrollAnchorProps {
  trackVisibility?: boolean;
}

export function ChatScrollAnchor({ trackVisibility }: ChatScrollAnchorProps) {
  const isAtBottom = useAtBottom();
  const { ref, entry, inView } = useInView({
    trackVisibility,
    delay: 100,
    rootMargin: '0px 0px -20px 0px',
  });

  useEffect(() => {
    if (isAtBottom && trackVisibility && !inView) {
      const container = entry?.target.parentElement;
      container?.classList.add('no-scrollbar');

      entry?.target.scrollIntoView({
        block: 'start',
        behavior: 'instant',
      });

      setTimeout(() => {
        container?.classList.remove('no-scrollbar');
      }, 500);
    }
  }, [inView, entry, isAtBottom, trackVisibility]);

  return (
    <div
      ref={ref}
      style={{
        width: '100%',
        height: '1px',
        msOverflowStyle: 'none',
        scrollbarWidth: 'none',
      }}
    >
      <style>
        {`
          .no-scrollbar {
            -ms-overflow-style: none;  /* IE and Edge */
            scrollbar-width: none;     /* Firefox */
          }

          .no-scrollbar::-webkit-scrollbar {
            display: none;  /* Chrome, Safari, and Opera */
          }
        `}
      </style>
    </div>
  );
}