import {Metadata, NextPage} from 'next';
import {Grid, Paper, Typography} from '@mui/material';

export const metadata: Metadata = {
  title: '_TITLE_',
  description: '_DESCRIPTION_',
};

export const applications = {
  "dev": {
    "name": "Eidolon Developer Tool",
    "description": "The developer tools can be used to test and debug any Eidolon operation.",
    "version": "0.1.0",
    "image": "/"
  }
}

const Item = () => {
  return (
    <Paper sx={{p: 2, textAlign: 'center'}}>
      <Typography variant="h6">xs=2</Typography>
    </Paper>
  )
}

/**
 * Main page of the Application
 * @page Home
 */
const Home: NextPage = () => {
  return (
    <Grid container spacing={{xs: 3, md: 3}} columns={{xs: 4, sm: 8, md: 12}}>
      {Array.from(Array(6)).map((_, index) => (
        <Grid item xs={2} sm={4} md={4} key={index}>
          <Item></Item>
        </Grid>
      ))}
    </Grid>
  );
};

export default Home;
