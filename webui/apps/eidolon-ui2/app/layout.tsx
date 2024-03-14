import {FunctionComponent, PropsWithChildren} from 'react';
import {Metadata, Viewport} from 'next';
import {SimplePaletteColorOptions} from '@mui/material';
import {AppStoreProvider} from '@/store';
import defaultTheme, {ThemeProvider} from '@/theme';
import CurrentLayout from '@/layout';
import './globals.css';
import {SessionProvider} from "next-auth/react";

const THEME_COLOR = (defaultTheme.palette?.primary as SimplePaletteColorOptions)?.main || '#FFFFFF';

export const metadata: Metadata = {
  title: 'Eidolon',
  description: 'Eidolon',
  manifest: '/site.webmanifest',
  // TODO: Add Open Graph metadata
};

export const viewport: Viewport = {
  themeColor: THEME_COLOR,
}

const RootLayout: FunctionComponent<PropsWithChildren> = ({children}) => {
  return (
    <html lang="en">
    <body>
    <SessionProvider>
      <AppStoreProvider>
        <ThemeProvider>
          <CurrentLayout>{children}</CurrentLayout>
        </ThemeProvider>
      </AppStoreProvider>
    </SessionProvider>
    </body>
    </html>
  );
};

export default RootLayout;
