'use client'

import * as React from 'react'
import {signIn} from 'next-auth/react'

import {cn} from '@/lib/utils'
import {IconGoogle, IconSpinner} from '@/components/ui/icons'
import {Button, ButtonProps} from '@mui/material'

interface LoginButtonProps extends ButtonProps {
  showGoogleIcon?: boolean
  text?: string
}

export function LoginButton({
                              text = 'Login with Google',
                              showGoogleIcon = true,
                              className,
                              ...props
                            }: LoginButtonProps) {
  const [isLoading, setIsLoading] = React.useState(false)
  return (
    <Button
      variant="outlined"
      onClick={() => {
        setIsLoading(true)
        // next-auth signIn() function doesn't work yet at Edge Runtime due to usage of BroadcastChannel
        signIn('google', {callbackUrl: `/`})
      }}
      disabled={isLoading}
      className={cn(className)}
      {...props}
    >
      {isLoading ? (
        <IconSpinner className="mr-2 animate-spin"/>
      ) : showGoogleIcon ? (
        <IconGoogle className="mr-2"/>
      ) : null}
      {text}
    </Button>
  )
}
