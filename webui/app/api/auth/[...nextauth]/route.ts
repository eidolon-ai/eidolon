// imports
import NextAuth, {type DefaultSession, NextAuthOptions} from "next-auth"

// importing providers
import GithubProvider from "next-auth/providers/github"
import GoogleProvider from "next-auth/providers/google";


declare module 'next-auth' {
  interface Session {
    user: {
      /** The user's id. */
      id: string
    } & DefaultSession['user']
  }
}

let authOptions: NextAuthOptions = {
  providers: [
    GithubProvider({
      clientId: process.env.GITHUB_ID as string,
      clientSecret: process.env.GITHUB_SECRET as string,
    }),
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID as string,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET as string,
    })
  ],
  callbacks: {
    jwt({token, profile}) {
      if (profile) {
        token.id = profile.sub
      }
      return token
    },
    session: async ({session, token}) => {
      if (session?.user && token) {
        session.user.id = token.id as string
      }
      return session
    },
  }
};
const handler = NextAuth(authOptions)

export {handler as GET, handler as POST, authOptions}
