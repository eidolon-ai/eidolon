import {Box, Breakpoint, useMediaQuery, useTheme} from "@mui/material";
import * as React from "react";

export interface FloatingColumnsProps {
  breakpoint?: Breakpoint
  rightVisible: boolean
  left: JSX.Element | ((breakpointMatches: boolean) => JSX.Element)
  right: JSX.Element | ((breakpointMatches: boolean) => JSX.Element)
}

export default function FloatingColumns({breakpoint, rightVisible, left, right}: FloatingColumnsProps) {
  const theme = useTheme();
  const matches = useMediaQuery(theme.breakpoints.up(breakpoint || 'lg'));

  return (
    <Box sx={{width: "100%", height: "100%", display: "flex", flexDirection: matches ? "row" : "column", overflow: "hidden"}}>
      <div style={{overflow: "hidden", flex: '0 0 ' + (rightVisible ? "50%" : "100%")}}>
        {typeof left === "function" ? left(matches) : left}
      </div>
      {rightVisible && (
        <div style={{flex: "0 0 50%", overflow: "hidden", display: "flex", justifyContent: "center", padding: "16px"}}>
          {typeof right === "function" ? right(matches) : right}
        </div>
      )}
    </Box>
  )
}
