import {Box} from "@mui/material";
import ResizableDrawer from "@/components/ResizableDrawer/ResizableDrawer";
import {DevProcessListWithAdd} from "./ProcessListWithAdd";
import {ProcessesProvider} from "@eidolon/components/src/hooks/process_context";
import {EidolonApp} from "@/utils/eidolon-apps";


export interface DevTooLayoutProps {
  app: EidolonApp
  children: JSX.Element
}

export function ProcessWithListLayout({children, app}: DevTooLayoutProps) {
  console.log("debugging: rendering ProcessWithListLayout")

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