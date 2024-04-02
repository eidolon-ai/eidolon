import {Box} from "@mui/material";
import ResizableDrawer from "@/components/ResizableDrawer/ResizableDrawer";
import {DevProcessListWithAdd} from "./ProcessListWithAdd";
import {ProcessesProvider} from "@eidolon/components/src/hooks/process_context";


export interface DevTooLayoutProps {
  agentName?: string
  children: JSX.Element
}

export function ProcessWithListLayout({agentName, children}: DevTooLayoutProps) {
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
          <DevProcessListWithAdd
            machineURL={process.env.EIDOLON_SERVER!}
            agentName={agentName}
          />
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