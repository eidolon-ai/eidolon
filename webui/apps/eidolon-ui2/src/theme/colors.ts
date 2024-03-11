import { PaletteOptions, SimplePaletteColorOptions } from '@mui/material';

const COLOR_PRIMARY: SimplePaletteColorOptions = {
  main: '#64B5F6',
  contrastText: '#000000',
  // light: '#64B5F6',
  // dark: '#64B5F6',
};

const COLOR_SECONDARY: SimplePaletteColorOptions = {
  main: '#EF9A9A',
  contrastText: '#000000',
  // light: '#EF9A9A',
  // dark: '#EF9A9A',
};

/**
 * MUI colors set to use in theme.palette
 */
export const PALETTE_COLORS: Partial<PaletteOptions> = {
  primary: COLOR_PRIMARY,
  secondary: COLOR_SECONDARY,
  // error: COLOR_ERROR,
  // warning: COLOR_WARNING;
  // info: COLOR_INFO;
  // success: COLOR_SUCCESS;
};
