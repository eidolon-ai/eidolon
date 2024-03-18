import {Metadata, NextPage} from 'next';
import {Paper} from '@mui/material';
import Grid from "@mui/material/Unstable_Grid2";
import {ReactNode} from "react";
import {getAppRegistry} from "@/utils/eidolon-apps";
import {EidolonAppItem} from "./EidolonAppItem";

export const metadata: Metadata = {
  title: 'Eidolon',
  description: 'Eidolon Home',
};


/**
 * Main page of the Application
 * @page Home
 */
const Home: NextPage = () => {
  const gridItems: ReactNode[] = []
  Object.entries(getAppRegistry()).forEach(([pathPart, app], index) => {
    gridItems.push((
      <Grid key={index} xs={12} sm={6} md={4} lg={3} xl={2}>
        <EidolonAppItem path={pathPart} app={app}/>
      </Grid>
    ))
  })

  return (
    <Paper
      elevation={0}
      sx={{
        padding: 2,
        margin: 2,
        textAlign: 'center',
        height: '100%',
      }}
    >
      <Grid container justifyContent={"space-evenly"} spacing={4}>
        {gridItems}
      </Grid>
    </Paper>
  )
}

export default Home;
