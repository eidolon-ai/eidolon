'use client'

import React, {MouseEvent, useCallback, useEffect, useRef} from "react";
import {Drawer, IconButton, styled} from "@mui/material";
import {DrawerProps} from "@mui/material/Drawer/Drawer";
import ChevronLeftIcon from "@mui/icons-material/ChevronLeft";
import ChevronRightIcon from "@mui/icons-material/ChevronRight";

export interface ResizableDrawerProps extends DrawerProps {
  defaultDrawerWidth?: number
  minDrawerWidth?: number
  maxDrawerWidth?: number
  updateRemainderWidth: (remainderWidth: number) => void
}

export default function ResizableDrawer({defaultDrawerWidth, maxDrawerWidth, minDrawerWidth, children, updateRemainderWidth, ...props}: ResizableDrawerProps) {
  if (!minDrawerWidth) {
    minDrawerWidth = 40
  }
  if (!maxDrawerWidth) {
    maxDrawerWidth = 1000
  }
  const [drawerWidth, setDrawerWidth] = React.useState(0);
  const childrenDivRef = useRef<HTMLDivElement>(null);
  const [loading, setLoading] = React.useState(true);

  useEffect(() => {
    // load the previous width from local storage
    const previousWidthStr = localStorage.getItem('drawerWidth');
    if (!previousWidthStr) {
      updateDrawerWidth(defaultDrawerWidth || 240)
    } else {
      let previousWidth = parseInt(previousWidthStr);
      setDrawerWidth(previousWidth)
      reportRemainingWidth(previousWidth)
    }

    window.addEventListener('resize', handleResize);

    setLoading(false)

    // Clean up the event listener on component unmount
    return () => {
      window.removeEventListener('resize', handleResize);
    }
  }, [childrenDivRef.current]);

  const handleResize = () => {
    reportRemainingWidth(drawerWidth)
  };

  function updateDrawerWidth(width: number, setLastOpened: boolean = true) {
    setDrawerWidth(width)
    localStorage.setItem('drawerWidth', `${width}`)
    if (setLastOpened) {
      localStorage.setItem('lastOpenedDrawerWidth', `${Math.max(width, minDrawerWidth!)}`)
    }
    reportRemainingWidth(width)
  }

  function reportRemainingWidth(newWidth: number) {
    const children = childrenDivRef.current;
    if (children) {
      const parentContainer = children.parentElement
      const parentWidth = parentContainer!.offsetWidth;
      const remainingWidth = parentWidth - Math.max(newWidth, minDrawerWidth!);
      updateRemainderWidth(remainingWidth)
    }
  }

  const handleMouseDown = () => {
    document.addEventListener("mouseup", handleMouseUp, true);
    // @ts-ignore
    document.addEventListener("mousemove", handleMouseMove, true);
  };

  const handleMouseUp = () => {
    document.removeEventListener("mouseup", handleMouseUp, true);
    // @ts-ignore
    document.removeEventListener("mousemove", handleMouseMove, true);
  };

  const handleMouseMove = useCallback((ev: MouseEvent): any => {
    const newWidth = ev.clientX - document.body.offsetLeft;
    if (newWidth >= minDrawerWidth! && newWidth < maxDrawerWidth!) {
      reportRemainingWidth(newWidth)
      updateDrawerWidth(newWidth);
    }
    ev.stopPropagation()
    ev.preventDefault()
  }, []);

  const DrawerFooter = styled('div')(({theme}) => ({
    display: 'flex',
    alignItems: 'center',
    // necessary for content to be below app bar
    ...theme.mixins.toolbar,
    justifyContent: 'flex-end',
  }));

  const handleDrawerOpen = () => {
    const lastOpenWidth = Math.max(minDrawerWidth!, parseInt(localStorage.getItem('lastOpenedDrawerWidth') || defaultDrawerWidth!.toString()));
    updateDrawerWidth(lastOpenWidth, false)
  };

  const handleDrawerClose = () => {
    updateDrawerWidth(0, false)
  };

  return (
    <Drawer
      ref={childrenDivRef}
      {...props}
      open={true}
      sx={{width: drawerWidth, minWidth: minDrawerWidth, height: '100%'}}
      PaperProps={{...props.PaperProps, elevation: 0, variant: "elevation", style: {display: 'flex', justifyContent: 'space-between', borderRight: '0px'}}}
    >
      <div style={{width: drawerWidth, minWidth: minDrawerWidth, height: '100%'}}>
        <div
          onMouseDown={() => handleMouseDown()}
          style={{
            display: drawerWidth > 0 ? 'block' : 'none',
            width: "5px",
            cursor: "ew-resize",
            borderTop: "1px solid #ddd",
            position: "absolute",
            top: 0,
            right: 0,
            bottom: 0,
            zIndex: 100,
            backgroundColor: "#f4f7f9"
          }}
        />
        {drawerWidth >= minDrawerWidth && (children)}
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
