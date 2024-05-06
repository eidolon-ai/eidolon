'use client';
import * as React from 'react';
import {FunctionComponent, PropsWithChildren} from 'react';
import {useRouter} from 'next/navigation';
import {Stack} from '@mui/material';
import ErrorBoundary from '../components/ErrorBoundary';
import TopBar from './TopBar';
import {LinkToPage} from '../utils/type';
import {useOnMobile} from '../hooks/index';
import {SIDEBAR_DESKTOP_ANCHOR, SIDEBAR_WIDTH, TOP_BAR_DESKTOP_HEIGHT, TOP_BAR_MOBILE_HEIGHT,} from './config';
import {EidolonHeader} from "../components/EidolonHeader";
import {RightSideBarItems} from "./RightSideBarItems";

const TITLE_PRIVATE = 'Eidolon'; // Title for pages after authentication

/**
 * SideBar navigation items with links
 */
const SIDE_BAR_ITEMS: Array<LinkToPage> = [
  {
    title: 'Home',
    path: '/',
    icon: 'home',
  },
  {
    title: 'Profile (404)',
    path: '/user',
    icon: 'account',
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
 * Renders "Private Layout" composition
 * @layout PrivateLayout
 */
const PrivateLayout: FunctionComponent<PropsWithChildren> = ({children}) => {
  const router = useRouter();
  const onMobile = useOnMobile();
  const shouldOpenSideBar = false;

  return (
    <Stack
      direction="column"
      sx={{
        minHeight: '100vh', // Full screen height
        paddingTop: onMobile ? TOP_BAR_MOBILE_HEIGHT : TOP_BAR_DESKTOP_HEIGHT,
        paddingLeft: shouldOpenSideBar && SIDEBAR_DESKTOP_ANCHOR.includes('left') ? SIDEBAR_WIDTH : 0,
        paddingRight: shouldOpenSideBar && SIDEBAR_DESKTOP_ANCHOR.includes('right') ? SIDEBAR_WIDTH : 0,
      }}
    >
      <Stack component="header">
        <TopBar
          startNode={EidolonHeader()}
          endNode={RightSideBarItems()}
          title={TITLE_PRIVATE}
          goToApp={
            () => {
              router.push('/dev')
            }
          }
        />
      </Stack>

      <Stack
        component="main"
        sx={{
          flexGrow: 1, // Takes all possible space
          paddingLeft: 1,
          paddingRight: 1,
          paddingTop: 1,
          height:`calc(100vh - ${onMobile ? TOP_BAR_MOBILE_HEIGHT : TOP_BAR_DESKTOP_HEIGHT})`
        }}
      >
        <ErrorBoundary name="Content">{children}</ErrorBoundary>
      </Stack>
    </Stack>
  );
};

export default PrivateLayout;
