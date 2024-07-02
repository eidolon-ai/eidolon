'use client'

import {Card, CardActionArea, CardContent, CardMedia, Typography} from "@mui/material";
import {useRouter} from "next/navigation";
import {EidolonApp} from "@eidolon/components/client";

export interface EidolonAppItemProps {
  path: string;
  app: EidolonApp;
}

export function EidolonAppItem({path, app}: EidolonAppItemProps) {
  const router = useRouter()
  return (
    <Card onClick={() => router.push(`/eidolon-apps/${path}`)}>
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
