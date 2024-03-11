'use client';
import { FunctionComponent, PropsWithChildren, useCallback, useState } from 'react';
import { Stack } from '@mui/material/';
import { AppIconButton } from '../components';
import BottomBar from './BottomBar';
import ErrorBoundary from '../components/ErrorBoundary';
import SideBar from './SideBar';
import TopBar from './TopBar';
import { LinkToPage } from '../utils/type';
import { useAppStore } from '../store';
import { useEventSwitchDarkMode, useOnMobile } from '../hooks';
import { BOTTOM_BAR_DESKTOP_VISIBLE, TOP_BAR_DESKTOP_HEIGHT, TOP_BAR_MOBILE_HEIGHT } from './config';

// TODO: change to your app name or other word
const TITLE_PUBLIC = '_TITLE_ app'; // Title for pages without/before authentication

/**
 * SideBar navigation items with links
 */
const SIDE_BAR_ITEMS: Array<LinkToPage> = [
  {
    title: 'Log In',
    path: '/auth/login',
    icon: 'login',
  },
  {
    title: 'Sign Up',
    path: '/auth/signup',
    icon: 'signup',
  },
  {
    title: 'About',
    path: '/about',
    icon: 'info',
  },
];

if (process.env.NEXT_PUBLIC_DEBUG) {
  SIDE_BAR_ITEMS.push({
    title: '[Debug Tools]',
    path: '/dev',
    icon: 'settings',
  });
}

/**
 * BottomBar navigation items with links
 */
const BOTTOM_BAR_ITEMS: Array<LinkToPage> = [
  {
    title: 'Log In',
    path: '/auth/login',
    icon: 'login',
  },
  {
    title: 'Sign Up',
    path: '/auth/signup',
    icon: 'signup',
  },
  {
    title: 'About',
    path: '/about',
    icon: 'info',
  },
];

/**
 * Renders "Public Layout" composition
 * @layout PublicLayout
 */
const PublicLayout: FunctionComponent<PropsWithChildren> = ({ children }) => {
  const onMobile = useOnMobile();
  const [sideBarVisible, setSideBarVisible] = useState(false);
  const [state] = useAppStore();
  const bottomBarVisible = onMobile || BOTTOM_BAR_DESKTOP_VISIBLE;
  const title = TITLE_PUBLIC;

  const onSwitchDarkMode = useEventSwitchDarkMode();

  const onSideBarOpen = useCallback(() => {
    if (!sideBarVisible) setSideBarVisible(true); // Don't re-render Layout when SideBar is already open
  }, [sideBarVisible]);

  const onSideBarClose = useCallback(() => {
    if (sideBarVisible) setSideBarVisible(false); // Don't re-render Layout when SideBar is already closed
  }, [sideBarVisible]);

  return (
    <Stack
      sx={{
        minHeight: '100vh', // Full screen height
        paddingTop: onMobile ? TOP_BAR_MOBILE_HEIGHT : TOP_BAR_DESKTOP_HEIGHT,
      }}
    >
      <Stack component="header">
        <TopBar
          startNode={<AppIconButton icon="logo" onClick={onSideBarOpen} />}
          title={title}
          endNode={
            <AppIconButton
              icon={state.darkMode ? 'day' : 'night'} // Variant 1
              // icon="daynight" // Variant 2
              title={state.darkMode ? 'Switch to Light mode' : 'Switch to Dark mode'}
              onClick={onSwitchDarkMode}
            />
          }
        />

        <SideBar
          anchor="left"
          open={sideBarVisible}
          variant="temporary"
          items={SIDE_BAR_ITEMS}
          onClose={onSideBarClose}
        />
      </Stack>

      <Stack
        component="main"
        sx={{
          flexGrow: 1, // Takes all possible space
          padding: 1,
        }}
      >
        <ErrorBoundary name="Content">{children}</ErrorBoundary>
      </Stack>

      <Stack component="footer">{bottomBarVisible && <BottomBar items={BOTTOM_BAR_ITEMS} />}</Stack>
    </Stack>
  );
};

export default PublicLayout;
