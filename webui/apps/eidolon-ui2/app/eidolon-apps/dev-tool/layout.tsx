import {Box} from "@mui/material";
import ResizableDrawer from "@/components/ResizableDrawer/ResizableDrawer";
import * as React from "react";
import {DevProcessListWithAdd} from "./components/ProcessListWithAdd";

export interface DevTooLayoutProps {
  children: React.ReactNode
}

export default function ({children}: DevTooLayoutProps) {
  return (
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
        <DevProcessListWithAdd
          machineURL={process.env.EIDOLON_SERVER!}
        />
      </ResizableDrawer>
      <Box component="main" flexGrow={1}>
        <Box height={"calc(100vh - 64px)"} display={"flex"} justifyContent={"center"}>
          {children}
        </Box>
      </Box>
    </Box>
  );

}