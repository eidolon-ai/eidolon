'use client';

import {createTheme, ThemeProvider} from '@mui/material/styles';

import {Roboto} from 'next/font/google';
import * as React from "react";
import {PropsWithChildren} from "react";
import {Box, CssBaseline, Drawer, Toolbar} from "@mui/material";
import {ProcessList} from "@/components/process-list";
import {Header} from "@/components/header";

const roboto = Roboto({
  weight: ['300', '400', '500', '700'],
  subsets: ['latin'],
  display: 'swap',
});

// const rootElement = document.getElementById("__next");

const lightTheme = createTheme({
  palette: {
    mode: 'light'
  },
  typography: {
    fontFamily: roboto.style.fontFamily,
    fontSize: 12,
  },
  components: {
    MuiFormControl: {
      defaultProps: {
        size: 'small', // This makes the form control condensed
        // margin: 'none',
        variant: 'standard',
        color: 'primary',
      },
    },
    MuiAppBar: {
      styleOverrides: {
        colorPrimary: {
          backgroundColor: "Background"
        }
      }
    }
  }
})

const darkTheme = createTheme({
  palette: {
    mode: 'light'
  },
  typography: {
    fontFamily: roboto.style.fontFamily,
  },
})

export {darkTheme, lightTheme}

export function MyProvider({children}: PropsWithChildren) {

  return (
    <ThemeProvider theme={lightTheme}>
      <Box sx={{display: 'flex'}}>
        <CssBaseline/>
        <Header></Header>
        <Drawer
          variant="permanent"
          sx={{
            width: 350,
            flexShrink: 0,
            [`& .MuiDrawer-paper`]: {width: 350, boxSizing: 'border-box'},
          }}
        >
          <Toolbar/>
          <ProcessList/>
        </Drawer>
        <Box component="main" flexGrow={1}>
          <Toolbar/>
          <Box height={"calc(100vh - 64px)"} display={"flex"} justifyContent={"center"}>
            {children}
          </Box>
        </Box>
      </Box>
    </ThemeProvider>
  )
}
