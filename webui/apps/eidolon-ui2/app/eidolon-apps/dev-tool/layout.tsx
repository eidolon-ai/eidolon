import {Box, Divider, ListItem, ListItemButton, ListItemIcon, ListItemText, Toolbar} from "@mui/material";
import ResizableDrawer from "@/components/ResizableDrawer/ResizableDrawer";
import List from "@mui/material/List";
import {AddCircleOutline} from "@mui/icons-material";
import {DevProcessList} from "./components/DevProcessList";

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
        <Box sx={{overflow: 'auto'}}>
          <Toolbar/>
          <List>
            <ListItem disablePadding>
              <ListItemButton>
                <ListItemIcon>
                  <AddCircleOutline/>
                </ListItemIcon>
                <ListItemText primary={"Add Chat"}/>
              </ListItemButton>
            </ListItem>
          </List>
          <Divider/>
          <DevProcessList/>
        </Box>
      </ResizableDrawer>
      <Box component="main" sx={{flexGrow: 1, p: 3}}>
        <Toolbar/>
        {children}
      </Box>

    </Box>
  );

}