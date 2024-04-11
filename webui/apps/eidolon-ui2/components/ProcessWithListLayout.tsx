import {Box} from "@mui/material";
import ResizableDrawer from "@/components/ResizableDrawer/ResizableDrawer";
import {DevProcessListWithAdd} from "./ProcessListWithAdd";
import {ProcessesProvider} from "@eidolon/components/src/hooks/process_context";
import {EidolonApp} from "@/utils/eidolon-apps";
import {EidolonClient} from "@eidolon/client";


export interface DevTooLayoutProps {
  app: EidolonApp
  children: JSX.Element
}

export async function ProcessWithListLayout({children, app}: DevTooLayoutProps) {
  // todo, there is a global client that will not need to make this request, we should use that instead
  const client = new EidolonClient(app.location)
  const agents = await client.getAgents()

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
          <DevProcessListWithAdd agents={agents} app={app} />
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