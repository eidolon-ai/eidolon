import {createContext, ReactNode, useContext, useState} from "react";

type HeaderContextType = {
  headerCenter: ReactNode | null;
  setHeaderCenter: React.Dispatch<React.SetStateAction<ReactNode | null>>;
}

const HeaderContext = createContext<HeaderContextType | undefined>(undefined)

type HeaderProviderProps = {
  children: ReactNode;
}

export function HeaderProvider({children}: HeaderProviderProps) {
  const [headerCenter, setHeaderCenter] = useState<ReactNode | null>(null)
  return (
    <HeaderContext.Provider value={{headerCenter, setHeaderCenter}}>
      {children}
    </HeaderContext.Provider>
  )
}

export function useHeader(): HeaderContextType {
  const context = useContext(HeaderContext)
  if (context === undefined) {
    throw new Error('useHeader must be used within a HeaderProvider')
  }
  return context
}
