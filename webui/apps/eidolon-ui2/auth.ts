import NextAuth, {type DefaultSession, NextAuthResult} from "next-auth"

import CredentialsProvider from "next-auth/providers/credentials";
import GithubProvider from "next-auth/providers/github"
import GoogleProvider from "next-auth/providers/google";
import {Provider} from "next-auth/providers";
import AzureADProvider from "next-auth/providers/microsoft-entra-id";
import {JWT} from "next-auth/jwt";
import qs from "qs"
import {NextResponse} from "next/server";

const providerTypes = (process.env.EIDOLON_AUTH_PROVIDERS?.trim().split(',') || []).filter(x => x.trim().length > 0)

export const providers: Provider[] = []

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

if (providerTypes.includes('password')) {
  providers.push(CredentialsProvider({
    credentials: {
      username: {label: "Username", type: "text", placeholder: "system"},
    },
    async authorize(credentials: Record<string, any> | undefined) {
      const name = credentials?.username || "system"
      return {id: name + "_id", name: name, email: name +'@b'}
    }
  }))
}

const nextAuth = NextAuth({
  providers: providers,
  pages: {
    signIn: "/signin",
  },
  basePath: '/api/auth',
  theme: {
    logo: "/img/eidolon_with_gradient.png",
    buttonText: "here",
  },
  callbacks: {
    async jwt({token, profile, session, user, account, trigger}) {
      if (trigger === "signIn" || trigger === "signUp") {
        if (token && profile) {
          if (profile.sub) {
            token.id = profile.sub
          } else {
            token.id = profile.id
          }
          token.access_token = account?.access_token!
        } else if (token?.sub) {
          token.id = token.sub
        }
      }

      if (account) {
        return {
          ...token,
          id: token.id,
          access_token: account.access_token,
          expires_at: account.expires_at || account.expires,
          refresh_token: account.refresh_token,
        } as JWT
      } else if (!token.expires_at) {
        return token
      } else if (Date.now() < token.expires_at * 1000) {
        // If the access token has not expired yet, return it
        return token
      } else {
        if (!token.refresh_token) throw new Error("Missing refresh token")

        // If the access token has expired, try to refresh it
        try {
          // https://accounts.google.com/.well-known/openid-configuration
          // We need the `token_endpoint`.
          const response = await fetch("https://oauth2.googleapis.com/token", {
            headers: {"Content-Type": "application/x-www-form-urlencoded"},
            body: new URLSearchParams({
              client_id: process.env.AUTH_GOOGLE_ID!,
              client_secret: process.env.AUTH_GOOGLE_SECRET!,
              grant_type: "refresh_token",
              refresh_token: token.refresh_token,
            }),
            method: "POST",
          })

          const tokens = await response.json()

          if (!response.ok) throw tokens

          return {
            ...token, // Keep the previous token properties
            access_token: tokens.access_token,
            expires_at: Math.floor(Date.now() / 1000 + tokens.expires_in),
            // Fall back to old refresh token, but note that
            // many providers may only allow using a refresh token once.
            refresh_token: tokens.refresh_token ?? token.refresh_token,
          }
        } catch (error) {
          console.error("Error refreshing access token", error)
          // The error property will be used client-side to handle the refresh token error
          return {...token, error: "RefreshAccessTokenError" as const}
        }
      }
    },
    session: async ({session, token}) => {
      if (session?.user && !session.user.id) {
        session.user.access_token = token?.access_token as string
        if (token?.id) {
          session.user.id = token.id as string
        } else {
          console.error("session.user.id not set", token)
        }
      }
      return session
    },
    authorized({request, auth}) {
      const {pathname} = request.nextUrl
      const currentURL = new URL(request.url)

      const parsedParams = qs.parse(currentURL.search, {ignoreQueryPrefix: true})

      const shouldAuth = providers.length > 0 && pathname.startsWith("/eidolon-apps")
      let authenticated = !!auth

      if (authenticated && pathname.startsWith("/signin") && "callbackUrl" in parsedParams) {
        return NextResponse.redirect(parsedParams["callbackUrl"] as string)
      } else if (authenticated || !shouldAuth) {
        return true
      } else {
        console.warn("Unauthorized request", request.url)
        return false
      }
    }
  }
})

export const {handlers, auth, signIn, signOut}: NextAuthResult = nextAuth

export interface EidolonProvider {
  id: string,
  type: string,
  style: string,
  name: string,
  credentials?: Record<string, any>,
}

export const providerMap = providers.map((inProvider) => {
  const provider = inProvider as any
  return {
    id: provider.id,
    type: provider.type,
    style: provider.style,
    name: provider.name,
    credentials: provider.options?.credentials,
  } as EidolonProvider
})

declare module 'next-auth' {
  interface Session {
    error?: "RefreshAccessTokenError"
    user: {
      /** The user's id. */
      id: string,
      access_token: string
    } & DefaultSession['user']
  }
}

declare module 'next-auth/jwt' {
  interface JWT {
    access_token: string
    expires_at: number
    refresh_token: string
    error?: "RefreshAccessTokenError"
  }
}
