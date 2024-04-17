import NextAuth, {type DefaultSession, User} from "next-auth"

import CredentialsProvider from "next-auth/providers/credentials";
import GithubProvider from "next-auth/providers/github"
import GoogleProvider from "next-auth/providers/google";
import {Provider} from "next-auth/providers/index";
import AzureADProvider from "next-auth/providers/azure-ad";
import type {NextAuthConfig} from "next-auth"

declare module 'next-auth' {
  interface Session {
    user: {
      /** The user's id. */
      id: string,
      access_token: string
    } & DefaultSession['user']
  }
}

const providerTypes = (process.env.EIDOLON_AUTH_PROVIDERS?.trim().split(',') || []).filter(x => x.trim().length > 0)

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
  providers.push(
    AzureADProvider({
      clientId: process.env.AZURE_CLIENT_ID || process.env.AZURE_AD_CLIENT_ID!,
      clientSecret: process.env.AZURE_CLIENT_SECRET || process.env.AZURE_AD_CLIENT_SECRET!,
      tenantId: process.env.AZURE_TENANT_ID || process.env.AZURE_AD_TENANT_ID,
      authorization: {
        params: {
          scope: "openid profile email " + process.env.AZURE_AD_PROFILE_EMAIL,
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
    async authorize(credentials: Record<string, any> | undefined) {
      return {id: "system", name: 'system', email: 'a@b'}
    }
  }))
}

export const config: NextAuthConfig = {
  providers: providers,
  basePath: '/api/auth',
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
    authorized({request, auth}) {
      const {pathname} = request.nextUrl
      let pathNameTest
      if (process.env.NEXT_PUBLIC_DEBUG) {
        pathNameTest = pathname.startsWith("/") && pathname !== "/"
      } else {
        pathNameTest = pathname.startsWith("/")
      }
      if (pathNameTest) return !!auth
      return true
    }
  }
} satisfies NextAuthConfig

export const {handlers, auth, signIn, signOut} = NextAuth(config)
