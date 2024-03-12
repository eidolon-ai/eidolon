'use client'

import * as React from 'react'
import {signOut, useSession} from "next-auth/react";
import {AppBar, Avatar, Box, Button, IconButton, Menu, MenuItem, Toolbar, Typography} from "@mui/material";
import {AccountCircle} from "@mui/icons-material";
import {useRouter} from "next/navigation";
import Link from 'next/link';

export function Header() {
  const {data: session} = useSession()
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
  const router = useRouter()

  const handleMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleSignout = async () => {
    await signOut({ redirect: false }).then(() => {
      router.push('/');
    });
    setAnchorEl(null);
  };
  

  const getIcon = () => {
    if (!session?.user?.image) {
      return <AccountCircle/>
    } else {
      return <Avatar sx={{height: "24px", width: "24px"}} src={session?.user?.image!}/>
    }
  }
  return (
    <AppBar position="fixed" sx={{zIndex: (theme) => theme.zIndex.drawer + 1}}>
      <Toolbar variant={"dense"}>
        <Button
          onClick={() => {
            router.push('/')
          }}
        >
        <Avatar src={"/eidolon_with_gradient.png"} sx={{height: "32px", width: "32px"}}/>
        <Typography variant="h5" component="div" sx={{marginLeft: '18px', display: {xs: 'none', sm: 'block'}, color: "darkgoldenrod"}} noWrap>
          Eidolon
        </Typography>
          </Button>
        <Box sx={{flexGrow: 1}}/>
        {session?.user && (
          <div>
            <IconButton
              size="small"
              aria-label="account of current user"
              aria-controls="menu-appbar"
              aria-haspopup="true"
              onClick={handleMenu}
            >
              {getIcon()}
            </IconButton>
            <Menu
              id="menu-appbar"
              anchorEl={anchorEl}
              anchorOrigin={{
                vertical: 'top',
                horizontal: 'right',
              }}
              keepMounted
              transformOrigin={{
                vertical: 'top',
                horizontal: 'right',
              }}
              open={Boolean(anchorEl)}
              onClose={handleClose}
            >
              <Link href="/profile">
                <MenuItem onClick={handleClose}>
                  Profile
                </MenuItem>
              </Link>
              <MenuItem onClick={handleSignout}>Sign out</MenuItem>
            </Menu>
          </div>
        )}
      </Toolbar>
    </AppBar>
  )
}