'use client'

import React, {createContext, useState, useContext} from 'react';
import {SelectedFile} from "@eidolon-ai/components/client";

export interface NewChatOptions {
  input: string,
  files: SelectedFile[],
  selectedLLM: string
  operation?: string
}

export interface NewChatOptionsContextType {
  options?: NewChatOptions;
  setOptions: (options: NewChatOptions) => void;
  clearOptions: () => void;
}

const NewChatOptionsContext = createContext<NewChatOptionsContextType | undefined>(undefined);

export function NewChatOptionsProvider({children}: { children: React.ReactNode }) {
  const [options, setOptions] = useState<NewChatOptions | undefined>(undefined);

  const clearOptions = () => {
    setOptions(undefined);
  }

  return (
    <NewChatOptionsContext.Provider value={{options, setOptions, clearOptions}}>
      {children}
    </NewChatOptionsContext.Provider>
  );
}

export function useNewChatOptions() {
  const context = useContext(NewChatOptionsContext);
  if (context === undefined) {
    throw new Error('useNewChatOptions must be used within a NewChatOptionsProvider');
  }
  return context;
}
