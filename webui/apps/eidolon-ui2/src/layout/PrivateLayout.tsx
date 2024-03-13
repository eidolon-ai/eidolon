'use client';
import * as React from 'react';
import {FunctionComponent, PropsWithChildren, useCallback, useState} from 'react';
import {useRouter} from 'next/navigation';
import {Avatar, Button, Stack, Typography} from '@mui/material';
import ErrorBoundary from '../components/ErrorBoundary';
import SideBar from './SideBar';
import TopBar from './TopBar';
import {LinkToPage} from '../utils/type';
import {useOnMobile} from '../hooks/index';
import {SIDEBAR_DESKTOP_ANCHOR, SIDEBAR_MOBILE_ANCHOR, SIDEBAR_WIDTH, TOP_BAR_DESKTOP_HEIGHT, TOP_BAR_MOBILE_HEIGHT,} from './config';
import {UserProfile} from "../components/UserProfile/UserProfile";
import {UsageIndicator} from "../components/UsageIndicator/UsageIndicator";

// TODO: change to your app name or other word
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

const RightSideBarItems = () => {
  return (
    <Stack direction="row" spacing={"16px"} alignItems={"center"} width={'240px'} minWidth={'240px'}>
      <UsageIndicator></UsageIndicator>
      <UserProfile/>
    </Stack>
  )
}

const HeaderStartItems = () => {
  const router = useRouter()
  return (
    <div style={{width: '240px', minWidth: '240px', display: 'flex', alignItems: 'center'}}>
      <Button
        onClick={() => {
          router.push('/')
        }}
      >
        <Avatar src={"/img/eidolon_with_gradient.png"} sx={{height: "32px", width: "32px"}}/>
      </Button>
      <Typography
        variant="h5"
        sx={{
          marginLeft: '0px',
          textAlign: 'left',
          whiteSpace: 'nowrap',
          color: "darkgoldenrod"
        }}
        noWrap
      >
        Eidolon
      </Typography>
    </div>
  )
}

/**
 * Renders "Private Layout" composition
 * @layout PrivateLayout
 */
const PrivateLayout: FunctionComponent<PropsWithChildren> = ({children}) => {
  const router = useRouter();
  const onMobile = useOnMobile();
  const [sideBarVisible, setSideBarVisible] = useState(false);
  const shouldOpenSideBar = false;
  const title = TITLE_PRIVATE;

  const onLogoClick = useCallback(() => {
    // Navigate to first SideBar's item or to '/' when clicking on Logo/Menu icon when SideBar is already visible
    router.push(SIDE_BAR_ITEMS?.[0]?.path || '/');
  }, [router]);

  const onSideBarOpen = useCallback(() => {
    if (!sideBarVisible) setSideBarVisible(true); // Don't re-render Layout when SideBar is already open
  }, [sideBarVisible]);

  const onSideBarClose = useCallback(() => {
    if (sideBarVisible) setSideBarVisible(false); // Don't re-render Layout when SideBar is already closed
  }, [sideBarVisible]);

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
          startNode={HeaderStartItems()}
          endNode={RightSideBarItems()}
          title={title}
          goToApp={
            () => {
              router.push('/dev')
            }
          }
        />

        <SideBar
          anchor={onMobile ? SIDEBAR_MOBILE_ANCHOR : SIDEBAR_DESKTOP_ANCHOR}
          open={shouldOpenSideBar}
          variant={onMobile ? 'temporary' : 'persistent'}
          items={SIDE_BAR_ITEMS}
          onClose={onSideBarClose}
        />
      </Stack>

      <Stack
        component="main"
        sx={{
          flexGrow: 1, // Takes all possible space
          paddingLeft: 1,
          paddingRight: 1,
          paddingTop: 1,
        }}
      >
        <ErrorBoundary name="Content">{children}</ErrorBoundary>
      </Stack>
    </Stack>
  );
};

export default PrivateLayout;
