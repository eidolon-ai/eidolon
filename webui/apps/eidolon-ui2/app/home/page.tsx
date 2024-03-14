import {Metadata, NextPage} from 'next';
import {Card, CardActionArea, CardContent, CardMedia, Paper, Typography} from '@mui/material';
import Grid from "@mui/material/Unstable_Grid2";
import {ReactNode} from "react";
import {EidolonApp, getAppRegistry} from "@/utils/eidolon-apps";

export const metadata: Metadata = {
  title: 'Eidolon',
  description: 'Eidolon Home',
};

const Item = ({path, app, ...rest}: { path: string, app: EidolonApp }) => {
  return (
    <Card>
      <CardActionArea>
        <CardMedia
          component="img"
          image={app.image}
          sx={{maxWidth: '100%'}}
          alt={app.name}
        />
        <CardContent>
          <Typography gutterBottom variant="h5" component="div">
            {app.name}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {app.description}
          </Typography>
        </CardContent>
      </CardActionArea>
    </Card>
  )
}

/**
 * Main page of the Application
 * @page Home
 */
const Home: NextPage = () => {
  const gridItems: ReactNode[] = []
  Object.entries(getAppRegistry()).forEach(([pathPart, app], index) => {
    gridItems.push((
      <Grid key={index} xs={12} sm={6} md={4} lg={3} xl={2}>
        <Item path={pathPart} app={app}/>
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
      <Grid container justifyContent={"space-evenly"} spacing={4} >
        {gridItems}
      </Grid>
    </Paper>
  )
}

export default Home;
