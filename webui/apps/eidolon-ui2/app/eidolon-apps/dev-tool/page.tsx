import {NextPage} from "next";
import {Box, Typography} from "@mui/material";

const DevTools: NextPage = () => {
  return (
    <Box component="main" sx={{flexGrow: 1, p: 3}}>
      <Typography paragraph>
        Welcome to the Dev tool UI. Put something interestng here
      </Typography>
    </Box>
  );
}

export default DevTools;
