'use client'

import React from 'react';
import { ArrowDownIcon } from 'lucide-react';
import { useAtBottom } from "../hooks/use-at-bottom.js";

export function ButtonScrollToBottom() {
  const isAtBottom = useAtBottom();

  const handleScrollToBottom = () => {
    const div = document.getElementById('chat-elements-scroll-region');
    if (div) {
      div.scrollTop = div.scrollHeight;
    }
  };

  if (!isAtBottom) {
    return (
      <button
        onClick={handleScrollToBottom}
        className="fixed bottom-4 right-4 p-2 bg-white rounded-full shadow-lg hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-200"
        aria-label="Scroll to bottom"
      >
        <ArrowDownIcon className="w-6 h-6 text-gray-600" />
      </button>
    );
  } else {
    return <div className="h-8" />;
  }
}
