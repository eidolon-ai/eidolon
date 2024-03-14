import {useRouter} from "next/navigation";
import {Avatar, Button, Typography} from "@mui/material";
import * as React from "react";

export const EidolonHeader = () => {
  const router = useRouter()
  return (
    <div style={{width: '240px', minWidth: '240px', display: 'flex', alignItems: 'center'}}>
      <Button
        onClick={() => {
          router.push('/')
        }}
      >
        <Avatar src={"/img/eidolon_with_gradient.png"} sx={{height: "32px", width: "32px"}}/>
      </Button>
      <Typography
        variant="h5"
        sx={{
          marginLeft: '0px',
          textAlign: 'left',
          whiteSpace: 'nowrap',
          color: "darkgoldenrod"
        }}
        noWrap
      >
        Eidolon
      </Typography>
    </div>
  )
}
