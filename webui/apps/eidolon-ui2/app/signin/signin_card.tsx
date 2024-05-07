'use client'

import {EidolonProvider} from "../../auth";
import {Box, Card, Divider, Link, Typography} from "@mui/material";
import SigninForm from "./SigninForm";
import {useSearchParams} from "next/navigation";

export interface SigninProps {
  providers: Record<string, EidolonProvider[]>
  doSignin: (providerId: string, formData: FormData) => Promise<void>
}

const signinErrors: Record<string, string> = {
  default: "Unable to sign in.",
  Signin: "Try signing in with a different account.",
  OAuthSignin: "Try signing in with a different account.",
  OAuthCallbackError: "Try signing in with a different account.",
  OAuthCreateAccount: "Try signing in with a different account.",
  EmailCreateAccount: "Try signing in with a different account.",
  Callback: "Try signing in with a different account.",
  OAuthAccountNotLinked:
    "To confirm your identity, sign in with the same account you used originally.",
  EmailSignin: "The e-mail could not be sent.",
  CredentialsSignin:
    "Sign in failed. Check the details you provided are correct.",
  SessionRequired: "Please sign in to access this page.",
}

export default function SigninCard({providers, doSignin}: SigninProps) {
  const params = useSearchParams()
  let error = undefined
  if (params.get("error")) {
    const errorValue = params.get("error")!
    error = signinErrors[errorValue] ?? signinErrors.default
  }
  return (
    <Card variant={"elevation"} sx={{padding: "32px"}}>
      <Typography fontWeight={"bold"} variant={"h5"} sx={{textAlign: "center", marginBottom: "1rem"}}>
        Eidolon Demo Cloud
      </Typography>
      {error && (
        <Typography color={"red"} variant={"body1"} sx={{marginBottom:"16px"}}>
          {error}
        </Typography>
      )}
      <Box sx={{display: "flex", flexDirection: "column"}}>
        {Object.keys(providers).map((providerType, index) => {
          return (
            <Box key={providerType} sx={{display: "flex", flexDirection: "column"}}>
              <Box sx={{marginBottom: "8px"}}>
                {providers[providerType]!.map((provider, index) => (
                  <SigninForm key={provider.id}
                              provider={{
                                id: provider.id,
                                type: provider.type,
                                style: provider.style,
                                name: provider.name,
                                credentials: provider.credentials,
                              }}
                              doSignin={doSignin}
                  />
                ))}
              </Box>
              {index < Object.keys(providers).length - 1 && <Divider sx={{margin: "1rem"}}>or</Divider>}
            </Box>
          )
        })}
      </Box>
      <Divider sx={{margin: "16px"}}/>
      <Typography variant={"body2"} sx={{textAlign: "center", margin: "1rem"}}>
        By logging in, you agree to our <Link href="http://www.eidolonai.com/terms">Terms of Service</Link>
      </Typography>
      <Typography variant={"body2"} sx={{textAlign: "center", marginTop: "1rem"}}>
        Have questions? <Link href="https://discord.gg/6kVQrHpeqG">Visit us on Discord</Link>
      </Typography>
    </Card>

  )
}