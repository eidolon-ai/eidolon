import {useRouter} from "next/navigation";
import {Avatar, Button, Typography} from "@mui/material";
import * as React from "react";
import BlackButton from "./BlackButton";

export const EidolonHeader = () => {
  const router = useRouter()
  return (
    <div style={{display: 'flex', alignItems: 'center'}}>
      <Button
        sx={{padding: 0, minWidth: "48px"}}
        onClick={() => {
          router.push('/')
        }}
      >
        <Avatar src={"/img/eidolon_with_gradient.png"} sx={{height: "32px", width: "32px"}}/>
      </Button>
      <Typography
        sx={{
          fontFamily: 'var(--aw-font-sans, ui-sans-serif),ui-sans-serif,system-ui,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji"',
          fontSize: '1.25rem',
          fontWeight: "bold",
          marginLeft: '0px',
          textAlign: 'left',
          whiteSpace: 'nowrap',
          marginRight: '16px'
        }}
        noWrap
      >
        Eidolon AI
      </Typography>
      <BlackButton href={"/"} variant={"text"} >Docs</BlackButton>
      <BlackButton href={"/"} variant={"text"} >Blog</BlackButton>
      <BlackButton href={"/"} variant={"text"} >Events</BlackButton>
    </div>
  )
}
