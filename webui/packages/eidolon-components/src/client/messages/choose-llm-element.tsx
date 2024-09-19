'use client'

import React from 'react';
import { ChevronDown } from 'lucide-react';

export interface ChooseLLMElementProps {
  supportedLLMs: string[] | undefined
  selectedLLM: string
  setSelectedLLM: (llm: string) => void
}

export const ChooseLLMElement: React.FC<ChooseLLMElementProps> = ({supportedLLMs, selectedLLM, setSelectedLLM}) => {
  if (!supportedLLMs) {
    return null;
  }

  return (
    <div className="relative inline-block w-full">
      <select
        className="block appearance-none w-full bg-white border border-gray-300 hover:border-gray-500 px-4 py-2 pr-8 rounded shadow leading-tight focus:outline-none focus:shadow-outline"
        value={selectedLLM}
        onChange={(event) => setSelectedLLM(event.target.value)}
      >
        {supportedLLMs.map(llm => (
          <option key={llm} value={llm}>{llm}</option>
        ))}
      </select>
      <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
        <ChevronDown size={20} />
      </div>
    </div>
  );
}