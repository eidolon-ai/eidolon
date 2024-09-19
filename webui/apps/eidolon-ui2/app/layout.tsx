import {FunctionComponent, PropsWithChildren} from 'react';
import {Metadata} from 'next';
import {AppStoreProvider} from '@/store';
import CurrentLayout from '@/layout';
import './globals.css';
import {SessionProvider} from "next-auth/react";
import {EidolonProvider} from "@eidolon-ai/components/client";
import {PHProvider} from "@/PosthogProvider.tsx";
import "@eidolon-ai/components/client-css";
import { Roboto } from 'next/font/google'

const font = Roboto({
  weight: ['400', '700'],
  subsets: ['latin'],
  display: 'swap',
})


export const metadata: Metadata = {
  title: 'Eidolon',
  description: 'Eidolon',
  // TODO: Add Open Graph metadata
};

const RootLayout: FunctionComponent<PropsWithChildren> = ({children}) => {
  return (
    <html lang="en" className={font.className}>
    <PHProvider>
      <body>
      <div className={"titanium-background"}/>
      <div className={"titanium-content"}>
        <SessionProvider>
          <AppStoreProvider>
            <EidolonProvider>
              <CurrentLayout>
                {children}
              </CurrentLayout>
            </EidolonProvider>
          </AppStoreProvider>
        </SessionProvider>
      </div>
      </body>
    </PHProvider>
    </html>
  );
};

export default RootLayout;
