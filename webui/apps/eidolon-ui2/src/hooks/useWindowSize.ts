import { useLayoutEffect, useState } from 'react';
import { IS_SERVER } from '@/utils';

const MOBILE_WINDOWS_SIZE = { width: 720, height: 1280 };
const DESKTOP_WINDOWS_SIZE = { width: 1920, height: 1080 };
const DEFAULT_WINDOWS_SIZE = MOBILE_WINDOWS_SIZE ?? DESKTOP_WINDOWS_SIZE; // Mobile-First by default

type WindowSize = {
  width: number;
  height: number;
};

/**
 * Hook to monitor Window (actually Browser) Size using "resize" event listener
 * @returns {WindowSize} current window size as {width, height} object
 */
const useWindowSize = (): WindowSize => {
  const [windowSize, setWindowSize] = useState<WindowSize>(DEFAULT_WINDOWS_SIZE);

  useLayoutEffect(() => {
    function handleResize() {
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    }

    window.addEventListener('resize', handleResize);
    handleResize(); // Get initial/current window size

    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return windowSize;
};

/**
 * The hook will really work in Browser only, so or Server Side Rendering (SSR) we just return DEFAULT_WINDOWS_SIZE
 */
export default IS_SERVER ? () => DEFAULT_WINDOWS_SIZE : useWindowSize;
