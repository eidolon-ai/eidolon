'use client'

import {Box} from "@mui/material";
import ResizableDrawer from "@/components/ResizableDrawer/ResizableDrawer";
import {DevProcessListWithAdd} from "./ProcessListWithAdd";
import {ProcessesProvider} from "../../../packages/eidolon-components/src/hooks/processes_context";
import {EidolonApp} from "@eidolon/components";
import {useEffect, useState} from "react";
import {getAgents} from "@eidolon/components/src/client-api-helpers/machine-helper";


export interface DevTooLayoutProps {
  app: EidolonApp
  children: JSX.Element
}

export function ProcessWithListLayout({children, app}: DevTooLayoutProps) {
  return (
    <ProcessesProvider>
      <Box sx={{
        display: 'flex'
      }}>
        <ResizableDrawer
          variant="persistent"
          sx={{
            flexShrink: 0,
            display: 'block',
            [`& .MuiDrawer-paper`]: {boxSizing: 'border-box'},
          }}
        >
          <DevProcessListWithAdd app={app} />
        </ResizableDrawer>
        <Box component="main" flexGrow={1}>
          <Box height={"calc(100vh - 64px)"} display={"flex"} justifyContent={"center"}>
            {children}
          </Box>
        </Box>
      </Box>
    </ProcessesProvider>
  );
}
