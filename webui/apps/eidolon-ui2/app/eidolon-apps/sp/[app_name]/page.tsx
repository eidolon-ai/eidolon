import {Box, Card, CardActionArea, CardContent, CardMedia, Typography} from "@mui/material";
import {getApp} from "@/utils/eidolon-apps";

export interface HomePageProps {
  params: {
    app_name: string
  }
}

const DevTools = ({params}: HomePageProps) => {
  const app = getApp(params.app_name)!
  return (
    <Box component="main" sx={{
      flexGrow: 1, p: 3, alignItems: "center", height: "100%", display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
    }}>
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
    </Box>
  );
}

export default DevTools;
