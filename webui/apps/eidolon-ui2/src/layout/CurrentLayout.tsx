'use client';
import React, {FunctionComponent, PropsWithChildren} from 'react';
import PrivateLayout from './PrivateLayout';

/**
 * Returns the current Layout component depending on different circumstances.
 * @layout CurrentLayout
 */
const CurrentLayout: FunctionComponent<PropsWithChildren> = (props) => {
  return <PrivateLayout {...props} />
};

export default CurrentLayout;
