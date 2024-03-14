'use client';
import * as React from 'react';
import {FunctionComponent, PropsWithChildren} from 'react';
import {Stack} from '@mui/material/';
import ErrorBoundary from '../components/ErrorBoundary';
import TopBar from './TopBar';
import {useOnMobile} from '../hooks';
import {TOP_BAR_DESKTOP_HEIGHT, TOP_BAR_MOBILE_HEIGHT} from './config';
import {useRouter} from "next/navigation";
import {EidolonHeader} from "../components/EidolonHeader";

const TITLE_PUBLIC = 'Eidolon'; // Title for pages without/before authentication

/**
 * Renders "Public Layout" composition
 * @layout PublicLayout
 */
const PublicLayout: FunctionComponent<PropsWithChildren> = ({children}) => {
  const onMobile = useOnMobile();
  const title = TITLE_PUBLIC;
  const router = useRouter();

  return (
    <Stack
      direction="column"
      sx={{
        minHeight: '100vh', // Full screen height
        paddingTop: onMobile ? TOP_BAR_MOBILE_HEIGHT : TOP_BAR_DESKTOP_HEIGHT,
        paddingLeft: 0,
        paddingRight: 0,
      }}
    >
      <Stack component="header">
        <TopBar
          startNode={EidolonHeader()}
          title={title}
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
        }}
      >
        <ErrorBoundary name="Content">{children}</ErrorBoundary>
      </Stack>
    </Stack>
  );
};

export default PublicLayout;
