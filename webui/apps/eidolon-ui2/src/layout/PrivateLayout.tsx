'use client';
import * as React from 'react';
import {FunctionComponent, PropsWithChildren} from 'react';
import ErrorBoundary from '../components/ErrorBoundary';
import {LinkToPage} from '../utils/type';
import {Header} from "./Header.tsx";
import {HeaderProvider} from "./HeaderContext.tsx";

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

  return (
    <div
      className={"flex flex-col overflow-hidden h-screen"}
    >
      <HeaderProvider>
        <Header/>
        <div
          className={"h-[inherit] overflow-hidden"}
        >
          <ErrorBoundary name="Content">{children}</ErrorBoundary>
        </div>
      </HeaderProvider>
    </div>
  );
};

export default PrivateLayout;
