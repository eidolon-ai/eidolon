'use client'

import {Box} from "@mui/material";
import ResizableDrawer from "@/components/ResizableDrawer/ResizableDrawer";
import {DevProcessListWithAdd} from "./ProcessListWithAdd";
import {ProcessesProvider} from "../../../packages/eidolon-components/src/hooks/processes_context";
import {EidolonApp} from "@eidolon/components";
import {useRef} from "react";


export interface DevTooLayoutProps {
  app: EidolonApp
  children: JSX.Element
}

export function ProcessWithListLayout({children, app}: DevTooLayoutProps) {
  const containerRef = useRef<HTMLDivElement>(null);

  function updateContainerWidth(newWidth: number) {
    if (containerRef.current) {
      containerRef.current.style.width = `${newWidth}px`
    }
  }

  return (
    <ProcessesProvider>
      <Box sx={{
        display: 'flex',
        height: '100%',
      }}>
        <ResizableDrawer
          updateRemainderWidth={updateContainerWidth}
          variant="persistent"
          sx={{
            display: 'block',
          }}
        >
          <DevProcessListWithAdd app={app} />
        </ResizableDrawer>
        <Box component="main" maxWidth={"100%"} ref={containerRef}>
          <Box height={"100%"} display={"flex"} justifyContent={"center"}>
            {children}
          </Box>
        </Box>
      </Box>
    </ProcessesProvider>
  );
}
