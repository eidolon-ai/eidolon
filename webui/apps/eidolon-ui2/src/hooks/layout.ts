import { useEffect, useState } from 'react';
import useWindowsSize from './useWindowSize';
import { useMediaQuery, useTheme } from '@mui/material';
import { IS_SERVER } from '@/utils';

export const MOBILE_SCREEN_MAX_WIDTH = 600; // Sync with https://mui.com/material-ui/customization/breakpoints/
export const SERVER_SIDE_ON_MOBILE_DEFAULT_VALUE = true; // true - for mobile, false - for desktop

/**
 * Hook to detect onMobile vs. onDesktop using "resize" event listener
 * @returns {boolean} true when on onMobile, false when on onDesktop
 */
export function useOnMobileByWindowsResizing() {
  const theme = useTheme();
  const { width } = useWindowsSize();
  const onMobile = width <= theme.breakpoints?.values?.sm ?? MOBILE_SCREEN_MAX_WIDTH;
  return onMobile;
}

/**
 * Hook to detect onMobile vs. onDesktop using Media Query
 * @returns {boolean} true when on onMobile, false when on onDesktop
 */
function useOnMobileByMediaQuery() {
  // const onMobile = useMediaQuery({ maxWidth: MOBILE_SCREEN_MAX_WIDTH });
  const theme = useTheme();
  const onMobile = useMediaQuery(theme.breakpoints.down('sm'));
  return onMobile;
}

/**
 * Hook to detect onMobile vs. onDesktop with Next.js workaround
 * @returns {boolean} true when on onMobile, false when on onDesktop
 */
function useOnMobileForNextJs() {
  // const onMobile = useOnMobileByWindowsResizing();
  const onMobile = useOnMobileByMediaQuery();
  const [onMobileDelayed, setOnMobileDelayed] = useState(SERVER_SIDE_ON_MOBILE_DEFAULT_VALUE);

  useEffect(() => {
    setOnMobileDelayed(onMobile); // Next.js don't allow to use useOnMobileXxx() directly, so we need to use this workaround
  }, [onMobile]);

  return onMobileDelayed;
}

/**
 * Hook to apply "onMobile" vs. "onDesktop" class to document.body depending on screen size.
 * Due to SSR/SSG we can not set 'app-layout onMobile' or 'app-layout onDesktop' on the server
 * If we modify className using JS, we will got Warning: Prop `className` did not match. Server: "app-layout" Client: "app-layout onDesktop"
 * So we have to apply document.body.class using the hook :)
 * Note: Use this hook one time only! In main App or Layout component
 */
function useMobileOrDesktopByChangingBodyClass() {
  // const onMobile = useOnMobileByWindowsResizing();
  const onMobile = useOnMobileByMediaQuery();

  useEffect(() => {
    if (onMobile) {
      document.body.classList.remove('onDesktop');
      document.body.classList.add('onMobile');
    } else {
      document.body.classList.remove('onMobile');
      document.body.classList.add('onDesktop');
    }
  }, [onMobile]);
}

/**
 * We need a "smart export wrappers", because we can not use hooks on the server side
 */
// export const useOnMobile = IS_SERVER ? () => SERVER_SIDE_IS_MOBILE_VALUE : useOnMobileByWindowsResizing;
// export const useOnMobile = IS_SERVER ? () => SERVER_SIDE_IS_MOBILE_VALUE : useOnMobileByMediaQuery;
export const useOnMobile = IS_SERVER ? () => SERVER_SIDE_ON_MOBILE_DEFAULT_VALUE : useOnMobileForNextJs;
export const useBodyClassForMobileOrDesktop = IS_SERVER ? () => undefined : useMobileOrDesktopByChangingBodyClass;
