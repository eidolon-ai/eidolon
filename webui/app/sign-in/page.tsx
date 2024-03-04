// mark as client component
"use client";

// importing necessary functions
import {signIn, useSession} from "next-auth/react"
import {redirect} from 'next/navigation'
import * as React from "react";
import {Box, Button, CircularProgress} from "@mui/material";
import {IconGitHub, IconGoogle} from "@/components/ui/icons";
import LoginIcon from '@mui/icons-material/Login';
import {getSigninOptions} from "@/app/sign-in/signon-options";

const providerMap: Record<string, [string, React.JSX.Element]> = {
  'google': ["Login with Google", <IconGoogle key="google" style={{height:"24px", width:"24px"}}/>],
  'github': ["Login with GitHub", <IconGitHub key="github" style={{height:"24px", width:"24px"}}/>],
  'noop': ["Login", <LoginIcon key="noop" style={{height:"24px", width:"24px"}}/>]
}

export default function SignInPage() {
  const {data: session} = useSession()
  const [isLoading, setIsLoading] = React.useState(false)
  const [providers, setProviders] = React.useState<string[]>([])
  React.useEffect(() => {
    getSigninOptions().then (signinOptions => {
      console.log(signinOptions)
      if (signinOptions.length === 0) {
        setProviders(['noop'])
      } else {
        setProviders(signinOptions)
      }
    })
  }, [])

  // redirect to home if user is already logged in
  if (session?.user) {
    redirect('/')
  }
  return (
    <div>
      {isLoading && <Box sx={{display: 'flex'}}><CircularProgress/></Box>}
      {!isLoading && providers.map(provider => {
        let [text, icon] = providerMap[provider]
        return (
          <Button
            key={provider}  // Add this line
            variant={"outlined"}
            startIcon={icon}
            onClick={() => {
              setIsLoading(true)
              signIn(provider, {callbackUrl: `/check`})
            }}
          >
            {text}
          </Button>
        )
      })}
    </div>
  )
}
