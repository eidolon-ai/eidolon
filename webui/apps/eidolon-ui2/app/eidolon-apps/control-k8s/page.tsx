import {NextPage} from "next";
import {Box, Typography} from "@mui/material";

const DevTools: NextPage = () => {
  return (
    <Box component="main" sx={{
      flexGrow: 1, p: 3, alignItems: "center", height: "100%", display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
    }}>
      <Typography paragraph variant={"h3"}>
        Eidolon Kubernetes Controller
      </Typography>
    </Box>
  );
}

export default DevTools;
