import NextAuth from "next-auth"
import GoogleProvider from "next-auth/providers/google"
import { NextAuthOptions } from "next-auth"

export const authOptions: NextAuthOptions = {
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
      authorization: {
        params: {
          hd: "growth-force.co.jp",
          prompt: "select_account"
        }
      }
    })
  ],
  callbacks: {
    async signIn({ account, profile }) {
      if (profile?.email?.endsWith("@growth-force.co.jp")) {
        return true
      }
      return false
    },
    async session({ session, token }) {
      if (session.user) {
        session.user.id = token.sub
      }
      return session
    }
  },
  pages: {
    signIn: "/login",
    error: "/auth/error"
  }
}

const handler = NextAuth(authOptions)
export { handler as GET, handler as POST }