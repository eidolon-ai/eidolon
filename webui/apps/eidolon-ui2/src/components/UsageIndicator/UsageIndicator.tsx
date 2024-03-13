import {Box, LinearProgress, Typography} from "@mui/material";
import * as React from "react";

export function UsageIndicator({...restOfProps}) {
  return (
    <Box sx={{display: 'flex', width: '100%', flexDirection: 'column', alignItems:"end"}} {...restOfProps}>
      <Box sx={{width: '100%', mr: 1, pt: "6px"}}>
        <LinearProgress sx={{height: '4px'}} variant="determinate" value={40}/>
      </Box>
      <Box sx={{minWidth: 35, textAlign: "right", paddingTop: '2px', mr:'9px'}}>
        <Typography variant="body2" color="text.secondary">35 / 60 minutes used</Typography>
      </Box>
    </Box>
  )
}
