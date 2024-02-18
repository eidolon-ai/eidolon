import {Metadata, Viewport} from 'next'

import '@/app/globals.css'
import * as React from "react";
import "@/app/layout-style.css"
import SessionWrapper from "@/components/session-wrapper";
import {AppRouterCacheProvider} from "@mui/material-nextjs/v13-appRouter";
import {MyProvider} from "@/app/theme";

export const metadata: Metadata = {
  metadataBase: new URL('https://eidolonai.com/'),
  title: {
    default: 'Eidolon AI Chatbot',
    template: `%s - Eidolon AI Chatbot`
  },
  description: 'An AI-powered chatbot for the Eidolon community.',
  icons: {
    icon: '/favicon.ico',
    shortcut: '/favicon-16x16.png',
    apple: '/apple-touch-icon.png'
  },
  openGraph: {
    images: '/og-image.png',
  },
}

export const viewport: Viewport = {
  themeColor: [
    {media: '(prefers-color-scheme: light)', color: 'white'},
    // {media: '(prefers-color-scheme: dark)', color: 'black'}
  ],
}

interface RootLayoutProps {
  children: React.ReactNode
}

export default function RootLayout({children}: RootLayoutProps) {
  return (
    <html lang="en" suppressHydrationWarning>
    <head><title>Eidolon</title></head>
    <body style={{overflow: "hidden", minHeight: "100vh"}}>
    <AppRouterCacheProvider options={{key: 'css', prepend: true}}>
      <SessionWrapper>
        <MyProvider>
          {children}
        </MyProvider>
      </SessionWrapper>
    </AppRouterCacheProvider>
    </body>
    </html>
  )
}
