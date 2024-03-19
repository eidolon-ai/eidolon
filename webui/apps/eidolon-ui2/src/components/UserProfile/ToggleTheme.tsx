'use client'


import {Box, ToggleButton, ToggleButtonGroup, Typography} from "@mui/material";
import * as React from "react";
import {useAppStore} from "../../store/index";

export function ToggleTheme() {
  const [state, dispatch] = useAppStore();

  const handleThemeChange = (_event: React.MouseEvent<HTMLElement>, newTheme: string) => {
    // setThemeMode(newTheme);
    state.darkMode = newTheme === "dark";
    state.themeMode = newTheme;
    dispatch({
      type: 'DARK_MODE',
      payload: newTheme,
    });
  }

  return (
    <Box>
      <Typography variant={"subtitle2"}>Theme</Typography>
      <ToggleButtonGroup
        color={"secondary"}
        size={"small"}
        value={state.themeMode}
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
  )
}