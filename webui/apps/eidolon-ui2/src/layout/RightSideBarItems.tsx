'use client'

import * as React from "react";
import {Button, Stack} from "@mui/material";
import {UsageIndicator} from "../components/UsageIndicator/UsageIndicator";
import {UserProfile} from "../components/UserProfile/UserProfile";
import {useIsAuthenticated} from "../hooks/index";
import {signIn} from "next-auth/react";
import BlackButton from "../components/BlackButton";

export const RightSideBarItems = () => {
  const [numStars, setNumStars] = React.useState("  ")
  const isAuthenticated = useIsAuthenticated()

  // React.useEffect(() => {
  //   fetch("https://api.github.com/repos/eidolon-ai/eidolon")
  //     .then((res) => res.json())
  //     .then((data) => {
  //       setNumStars(data.stargazers_count)
  //     })
  // }, [])
  return (
    <Stack direction="row" spacing={"16px"} alignItems={"center"} justifyContent={"flex-end"}>
      <BlackButton
        href="https://github.com/eidolon-ai/eidolon"
        variant={"text"}
        sx={{textWrap: "nowrap"}}
      >Star on GitHub ⭐</BlackButton>
      <BlackButton
        href="https://discord.gg/6kVQrHpeqG"
        sx={{textWrap: "nowrap", margin: 0}}
        variant="text"
        endIcon={(
          <img src='https://assets-global.website-files.com/6257adef93867e50d84d30e2/653714c174fc6c8bbea73caf_636e0a69f118df70ad7828d4_icon_clyde_blurple_RGB.svg' alt="Discord"
               height={20} width={20}
          />
        )}>Join us on Discord
      </BlackButton>
      {isAuthenticated && <UsageIndicator/>}
      {isAuthenticated && <UserProfile/>}
      {!isAuthenticated && <BlackButton
          onClick={() => signIn()}
          sx={{borderRadius: "9999px", textWrap: "nowrap", borderColor: "rgb(156, 163, 175)", paddingLeft: "16px", paddingRight: "16px"}}
          variant="text">Login
      </BlackButton>}
    </Stack>
  )
}