'use client';
import React, { FunctionComponent, PropsWithChildren } from 'react';
import { useIsAuthenticated } from '../hooks';
import PrivateLayout from './PrivateLayout';
import PublicLayout from './PublicLayout';

/**
 * Returns the current Layout component depending on different circumstances.
 * @layout CurrentLayout
 */
const CurrentLayout: FunctionComponent<PropsWithChildren> = (props) => {
  return useIsAuthenticated() ? <PrivateLayout {...props} /> : <PublicLayout {...props} />;
};

export default CurrentLayout;
