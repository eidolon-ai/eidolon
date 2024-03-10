// imports
import NextAuth from "next-auth"

// importing providers
import authOptions from "@/app/api/auth/[...nextauth]/authOptions";


const handler = NextAuth(authOptions)

export {handler as GET, handler as POST}
