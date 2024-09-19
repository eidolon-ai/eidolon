'use client'

import {ReactNode} from 'react';
import {ChevronRight, Pin} from 'lucide-react';
import {useMouseTracking} from "../utils/mouseDetection.ts";

interface DrawerSidebarProps {
  children: ReactNode;
}

export const DrawerSidebar: React.FC<DrawerSidebarProps> = ({children}) => {
  const initialIsPinned = localStorage.getItem('sidebarPinned') === 'true';
  const { ref, isMouseOver, isPinned, setIsPinned } = useMouseTracking({
    initialIsPinned,
    onMouseEnter: () => {},
    onMouseLeave: () => {},
  });

  const togglePin = (): void => {
    const value = !isPinned;
    localStorage.setItem('sidebarPinned', JSON.stringify(value));
    setIsPinned(value);
  };

  const forceClose = (): void => {

  }

  return (
    <>
      <div ref={ref}
        className={`${isPinned ? 'relative' : 'absolute'} z-50 h-full left-0 transition-all duration-300 ease-in-out backdrop-blur-md ${
          isMouseOver || isPinned ? 'min-w-[calc(100vw/4)] shadow-lg bg-white bg-opacity-30' : 'w-12'
        }`}
      >
        <div className="flex flex-col h-full relative">
          {(isMouseOver || isPinned) && (
            <>
              <div className={`absolute top-2 right-2 z-50`}>
                <button
                  onClick={togglePin}
                  className={`p-1 rounded-full ${
                    isPinned ? 'bg-blue-100 text-blue-600' : 'text-gray-400 hover:text-gray-600'
                  }`}
                >
                  <Pin size={16} className={isPinned ? 'align-middle rotate-45' : 'align-middle'}/>
                </button>
              </div>
              <div className="flex-grow overflow-y-auto p-4">
                {children}
              </div>
            </>
          )}
          <div className="absolute bottom-4 w-full flex justify-end items-center pr-2">
            <ChevronRight
              size={20}
              className={`text-gray-400 hover:text-gray-600 transition-all duration-300 cursor-pointer ${
                isMouseOver || isPinned ? 'rotate-180' : ''
              }`}
              onClick={forceClose}
            />
          </div>
        </div>
      </div>
    </>
  );
};

