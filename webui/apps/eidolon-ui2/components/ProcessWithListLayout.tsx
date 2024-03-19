import {Box} from "@mui/material";
import ResizableDrawer from "@/components/ResizableDrawer/ResizableDrawer";
import * as React from "react";
import {PropsWithChildren} from "react";
import {DevProcessListWithAdd} from "./ProcessListWithAdd";

export interface DevTooLayoutProps extends PropsWithChildren {
  agentName?: string
}

export function ProcessWithListLayout(props: DevTooLayoutProps) {
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
          agentName={props.agentName}
        />
      </ResizableDrawer>
      <Box component="main" flexGrow={1}>
        <Box height={"calc(100vh - 64px)"} display={"flex"} justifyContent={"center"}>
          {props.children}
        </Box>
      </Box>
    </Box>
  );

}