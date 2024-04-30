import {Avatar, Box, Divider, Drawer, IconButton, ListItem, Paper, Tooltip, Typography} from "@mui/material";
import * as React from "react";
import {useSession} from "next-auth/react";
import {AccountCircle, Close} from "@mui/icons-material";
import { signOut } from "next-auth/react"
import {useRouter} from "next/navigation";
import List from "@mui/material/List";
import Button from "@mui/material/Button";
import {UsageIndicator} from "../UsageIndicator/UsageIndicator";
import {ToggleTheme} from "./ToggleTheme";

export const UserProfile = () => {
  const {data: session} = useSession()
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
  const router = useRouter()
  const [drawerOpen, setDrawerOpen] = React.useState(false);

  const handleMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleProfile = () => {
    setAnchorEl(null);
    router.push("/user/profile")
  };

  const handleSignout = async () => {
    setAnchorEl(null);
    await signOut()
  };

  const getIcon = () => {
    if (!session?.user?.image) {
      return <AccountCircle/>
    } else {
      return <Avatar sx={{height: "32px", width: "32px"}} src={session?.user?.image!}/>
    }
  }
  const toggleDrawer =
    (open: boolean) =>
      (event: React.KeyboardEvent | React.MouseEvent) => {
        if (
          event.type === 'keydown' &&
          ((event as React.KeyboardEvent).key === 'Tab' ||
            (event as React.KeyboardEvent).key === 'Shift')
        ) {
          return;
        }

        setDrawerOpen(open);
      };

  const list = () => (
    <Paper
      square={false}
      sx={{width: 250, height: '100%', display: "flex", flexDirection: "column", justifyContent: "space-between"}}
      role="presentation"
      onKeyDown={toggleDrawer(false)}
    >
        <div>
          <List>
            <ListItem
              secondaryAction={
                <IconButton
                  edge="end"
                  onClick={toggleDrawer(false)}
                  aria-label="close">
                  <Close/>
                </IconButton>
              }
            >
              Profile
            </ListItem>
          </List>
          <Divider/>
          <List>
            <ListItem>
              <ToggleTheme/>
            </ListItem>
          </List>
          <Divider/>
            <List>
              <ListItem>
                <Typography variant="subtitle1">Eidolon Time</Typography>
              </ListItem>
              <ListItem>
                <UsageIndicator />
              </ListItem>
              <ListItem>
                <Box>
                  <Button variant={"outlined"} color={"secondary"}>
                    Request more Time
                  </Button>
                </Box>
              </ListItem>
            </List>
            <Divider/>
        </div>
        <Button variant={"outlined"} color={"primary"}
                sx={{margin: "0px 8px 16px 8px"}}
                onClick={handleSignout}
        >
          Sign out
        </Button>
    </Paper>
  );

  return (
    <div>
      <Tooltip title={"User Settings"}>
        <IconButton
          size="small"
          aria-label="account of current user"
          aria-controls="menu-appbar"
          aria-haspopup="true"
          onClick={toggleDrawer(true)}
        >
          {getIcon()}
        </IconButton>
      </Tooltip>
      <Drawer
        anchor={"right"}
        open={drawerOpen}
        onClose={toggleDrawer(false)}

      >
        {list()}
      </Drawer>
    </div>
  )
}
