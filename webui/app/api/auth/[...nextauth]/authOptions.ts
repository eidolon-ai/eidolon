import {type DefaultSession, NextAuthOptions, User} from "next-auth"
import CredentialsProvider from "next-auth/providers/credentials";
import GithubProvider from "next-auth/providers/github"
import GoogleProvider from "next-auth/providers/google";
import {Provider} from "next-auth/providers";
import AzureADProvider from "next-auth/providers/azure-ad";

declare module 'next-auth' {
  interface Session {
    user: {
      /** The user's id. */
      id: string,
      access_token: string
    } & DefaultSession['user']
  }
}

const providerTypes = process.env.EIDOLON_AUTH_PROVIDERS?.split(',') || []

const providers: Provider[] = []

if (providerTypes.includes('github')) {
  providers.push(GithubProvider({
    clientId: process.env.GITHUB_ID as string,
    clientSecret: process.env.GITHUB_SECRET as string,
  }))
}

if (providerTypes.includes('google')) {
  providers.push(GoogleProvider({
    clientId: process.env.GOOGLE_CLIENT_ID as string,
    clientSecret: process.env.GOOGLE_CLIENT_SECRET as string,
  }))
}

if (providerTypes.includes('azure')) {
  const default_scope = process.env.AZURE_AD_CLIENT_ID + "/.default"
  providers.push(
    AzureADProvider({
      clientId: process.env.AZURE_AD_CLIENT_ID!,
      clientSecret: process.env.AZURE_AD_CLIENT_SECRET!,
      tenantId: process.env.AZURE_AD_TENANT_ID,
      authorization: {
        params: {
          scope: `openid profile email ${default_scope}`,
        },
      }
    }),
  )
}

if (providerTypes.length === 0) {
  providers.push(CredentialsProvider({
    id: "credentials",
    type: "credentials",
    name: 'Credentials',
    credentials: {
      username: {label: "Username", type: "text", placeholder: "system"},
    },
    async authorize(credentials: Record<"username", string> | undefined) {
      return {id: "system", name: 'system', email: 'a@b'} as User
    }
  }))
}

let authOptions: NextAuthOptions = {
  providers: providers,
  callbacks: {
    jwt({token, profile, session, user, account, trigger}) {
      if (trigger === "signIn" || trigger === "signUp") {
        if (token && profile) {
          token.id = profile.sub
          token.access_token = account!.access_token
        } else if (token?.sub) {
          token.id = token.sub
        }
      }
      return token
    },
    session: async ({session, token}) => {
      if (session?.user && !session.user.id) {
        session.user.access_token = token?.access_token as string
        if (token?.id) {
          session.user.id = token.id as string
        } else {
          console.log("session.user.id not set", token)
        }
      }
      return session
    },
  }
};
export default authOptions;