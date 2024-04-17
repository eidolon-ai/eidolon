import {Metadata, NextPage} from 'next';
import {Paper} from '@mui/material';
import Grid from "@mui/material/Unstable_Grid2";
import {getAppRegistry} from "@/utils/eidolon-apps";
import {EidolonAppItem} from "./EidolonAppItem";

export const revalidate = 0

export const metadata: Metadata = {
  title: 'Eidolon',
  description: 'Eidolon Home',
};


/**
 * Main page of the Application
 * @page Home
 */
const Home: NextPage = () => {
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
        {Object.values(getAppRegistry()).map((app, index) => (
          <Grid key={index} xs={12} sm={6} md={4} lg={3} xl={2}>
            <EidolonAppItem path={app.path} app={app}/>
          </Grid>
        ))}
      </Grid>
    </Paper>
  )
}

export default Home;
