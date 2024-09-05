import {FunctionComponent, PropsWithChildren} from 'react';
import {Metadata, Viewport} from 'next';
import {SimplePaletteColorOptions} from '@mui/material';
import {AppStoreProvider} from '@/store';
import defaultTheme, {ThemeProvider} from '@/theme';
import CurrentLayout from '@/layout';
import './globals.css';
import {SessionProvider} from "next-auth/react";
import {EidolonProvider} from "@eidolon-ai/components/client";
import {PHProvider} from "@/PosthogProvider.tsx";

const THEME_COLOR = (defaultTheme.palette?.primary as SimplePaletteColorOptions)?.main || '#FFFFFF';

export const metadata: Metadata = {
  title: 'Eidolon',
  description: 'Eidolon',
  // TODO: Add Open Graph metadata
};

export const viewport: Viewport = {
  themeColor: THEME_COLOR,
}

const RootLayout: FunctionComponent<PropsWithChildren> = ({children}) => {
  return (
    <html lang="en">
    <PHProvider>
      <body>
      <SessionProvider>
        <AppStoreProvider>
          <EidolonProvider>
            <ThemeProvider>
              <CurrentLayout>
                {children}
              </CurrentLayout>
            </ThemeProvider>
          </EidolonProvider>
        </AppStoreProvider>
      </SessionProvider>
      </body>
    </PHProvider>
    </html>
  );
};

export default RootLayout;
