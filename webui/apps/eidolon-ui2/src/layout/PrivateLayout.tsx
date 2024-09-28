'use client';
import * as React from 'react';
import {FunctionComponent, PropsWithChildren} from 'react';
import ErrorBoundary from '../components/ErrorBoundary';
import {Header} from "./Header.tsx";
import {HeaderProvider} from "./HeaderContext.tsx";

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
