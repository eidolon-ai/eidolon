'use client'

import React, {MouseEvent, useCallback} from "react";
import {Drawer, IconButton, styled} from "@mui/material";
import {DrawerProps} from "@mui/material/Drawer/Drawer";
import ChevronLeftIcon from "@mui/icons-material/ChevronLeft";
import ChevronRightIcon from "@mui/icons-material/ChevronRight";

export interface ResizableDrawerProps extends DrawerProps {
  defaultDrawerWidth?: number
  minDrawerWidth?: number
  maxDrawerWidth?: number
}

export default function ResizableDrawer({defaultDrawerWidth, maxDrawerWidth, minDrawerWidth, children, ...props}: ResizableDrawerProps) {
  if (!defaultDrawerWidth) {
    defaultDrawerWidth = 240
  }
  if (!minDrawerWidth) {
    minDrawerWidth = 58
  }
  if (!maxDrawerWidth) {
    maxDrawerWidth = 1000
  }
  const [drawerWidth, setDrawerWidth] = React.useState(defaultDrawerWidth);
  const [lastOpenWidth, setLastOpenWidth] = React.useState(defaultDrawerWidth);

  const handleMouseDown = () => {
    document.addEventListener("mouseup", handleMouseUp, true);
    document.addEventListener("mousemove", handleMouseMove, true);
  };

  const handleMouseUp = () => {
    document.removeEventListener("mouseup", handleMouseUp, true);
    document.removeEventListener("mousemove", handleMouseMove, true);
  };

  const handleMouseMove = useCallback((ev: MouseEvent): any => {
    const newWidth = ev.clientX - document.body.offsetLeft;
    if (newWidth >= minDrawerWidth! && newWidth < maxDrawerWidth!) {
      setDrawerWidth(newWidth);
      setLastOpenWidth(newWidth)
    }
  }, []);

  const DrawerFooter = styled('div')(({theme}) => ({
    display: 'flex',
    alignItems: 'center',
    padding: theme.spacing(0, 1),
    // necessary for content to be below app bar
    ...theme.mixins.toolbar,
    justifyContent: 'flex-end',
  }));

  const handleDrawerOpen = () => {
    if (lastOpenWidth <= minDrawerWidth!) {
      setLastOpenWidth(defaultDrawerWidth!)
    }
    setDrawerWidth(lastOpenWidth)
  };

  const handleDrawerClose = () => {
    setDrawerWidth(minDrawerWidth!)
  };

  return (
    <Drawer
      {...props}
      sx={{width: drawerWidth}}
      open={true}
      PaperProps={{...props.PaperProps, style: {width: drawerWidth, display: 'flex', justifyContent: 'space-between'}}}
    >
      <div>
        <div
          onMouseDown={() => handleMouseDown()}
          style={{
            width: "5px",
            cursor: "ew-resize",
            padding: "4px 0 0",
            borderTop: "1px solid #ddd",
            position: "absolute",
            top: 0,
            right: 0,
            bottom: 0,
            zIndex: 100,
            backgroundColor: "#f4f7f9"
          }}
        />
        {children}
      </div>
      <DrawerFooter>
        <IconButton
          onClick={handleDrawerClose}
          sx={{display: drawerWidth <= minDrawerWidth ? 'none' : 'block'}}
        >
          <ChevronLeftIcon/>
        </IconButton>
        <IconButton
          onClick={handleDrawerOpen}
          sx={{display: drawerWidth <= minDrawerWidth ? 'block' : 'none'}}
        >
          <ChevronRightIcon/>
        </IconButton>
      </DrawerFooter>
    </Drawer>
  );
}
