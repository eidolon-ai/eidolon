import {EidolonProvider, providerMap, signIn} from "../../auth";
import SigninCard from "./signin_card";

export const revalidate = 0

export default function SignInPage() {
  const providers: Record<string, EidolonProvider[]> = {
    "credentials": [],
    "oauth": [],
  }
  for (const provider of providerMap) {
    const key = provider.type == "oauth" || provider.type == "oidc" ? "oauth" : provider.type
    if (!providers[key]) {
      providers[key] = []
    }

    providers[key]!.push({
      id: provider.id,
      type: provider.type,
      style: provider.style,
      name: provider.name,
      credentials: provider.credentials,
    })
  }

  if (providers["credentials"] && providers["credentials"].length === 0) {
    delete providers["credentials"]
  }

  if (providers["oauth"] && providers["oauth"].length === 0) {
    delete providers["oauth"]
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-200">
      <SigninCard providers={providers} doSignin={
        async (providerId: string, formData: FormData) => {
          "use server"
          await signIn(providerId, formData)
        }}/>
    </div>
  )
}
