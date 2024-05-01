'use client'

import {Box, CircularProgress, CircularProgressProps} from "@mui/material";
import {SxProps} from "@mui/material/styles";

export function CircularProgressWithContent(
  props: CircularProgressProps & { sx?: SxProps, children: JSX.Element }
) {
  return (
    <Box sx={{position: 'relative', display: 'inline-flex', alignItems: 'center', ...(props.sx || {})}}>
      <CircularProgress {...props} />
      <Box
        sx={{
          top: 0,
          left: 0,
          bottom: 0,
          right: 0,
          position: 'absolute',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        {props.children}
      </Box>
    </Box>
  );
}
