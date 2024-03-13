import {Avatar, Box, Divider, Drawer, IconButton, LinearProgress, ListItem, Paper, ToggleButton, ToggleButtonGroup, Tooltip, Typography} from "@mui/material";
import * as React from "react";
import {useSession} from "next-auth/react";
import {AccountCircle, Close} from "@mui/icons-material";
import {signOut} from "../../../auth";
import {useRouter} from "next/navigation";
import List from "@mui/material/List";
import Button from "@mui/material/Button";
import {UsageIndicator} from "../UsageIndicator/UsageIndicator";

export const UserProfile = () => {
  const {data: session} = useSession()
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
  const router = useRouter()
  const [theme, setTheme] = React.useState("light");
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

  const handleThemeChange = (event: React.MouseEvent<HTMLElement>, newTheme: string | null) => {
    setTheme(newTheme!);
  }

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
              <Box>
                <Typography variant={"subtitle2"}>Theme</Typography>
                <ToggleButtonGroup
                  color={"secondary"}
                  size={"small"}
                  value={theme}
                  exclusive
                  onChange={handleThemeChange}
                  aria-label="text alignment"
                >
                  <ToggleButton value="light" aria-label="left aligned">
                    Light
                  </ToggleButton>
                  <ToggleButton value="system" aria-label="centered">
                    System
                  </ToggleButton>
                  <ToggleButton value="dark" aria-label="right aligned">
                    Dark
                  </ToggleButton>
                </ToggleButtonGroup>
              </Box>
            </ListItem>
          </List>
          <Divider/>
          <List>
            <ListItem>
              <Typography variant={"subtitle1"}>Eidlon Time</Typography>
            </ListItem>
            <ListItem>
              <UsageIndicator></UsageIndicator>
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
      {/*      <Menu
        id="menu-appbar"
        anchorEl={anchorEl}
        anchorOrigin={{
          vertical: 'bottom',
          horizontal: 'left',
        }}
        keepMounted
        transformOrigin={{
          vertical: 'top',
          horizontal: 'left',
        }}
        open={Boolean(anchorEl)}
        onClose={handleClose}
        slotProps={{
          paper: {
            "style": {
              "width": "180px"
            }
          }
        }}
      >
        <MenuList>
          <MenuItem>
            <ToggleButtonGroup
              size={"small"}
              value={theme}
              exclusive
              onChange={handleThemeChange}
              aria-label="text alignment"
            >
              <ToggleButton value="light" aria-label="left aligned">
                Light
              </ToggleButton>
              <ToggleButton value="system" aria-label="centered">
                System
              </ToggleButton>
              <ToggleButton value="dark" aria-label="right aligned">
                Dark
              </ToggleButton>
            </ToggleButtonGroup>
          </MenuItem>
          <MenuItem onClick={handleProfile}>Profile</MenuItem>
          <MenuItem onClick={handleSignout}>Sign out</MenuItem>
        </MenuList>
      </Menu>*/}
    </div>
  )
}
