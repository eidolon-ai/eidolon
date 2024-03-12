import {type DefaultSession, NextAuthOptions, User} from "next-auth"
import CredentialsProvider from "next-auth/providers/credentials";
import GithubProvider from "next-auth/providers/github"
import GoogleProvider from "next-auth/providers/google";
import {Provider} from "next-auth/providers";
import {createConnection} from "mysql2/promise";
import {RowDataPacket} from "mysql2";
import {config} from "dotenv";

declare module 'next-auth' {
    interface Session {
        user: {
            /** The user's id. */
            id: string
        } & DefaultSession['user']
    }
}

config();
interface DbConfig {
    host: string;
    user: string;
    password: string;
    database: string;
    port: number;
    ssl: {
        ca: string;
    };
}
const databaseName = process.env.DB_NAME || "crimebot";

// Assuming you've saved your CA certificate to a file, you read it like this:
const caCert = process.env.CA_CERT;

const dbConfig: DbConfig = {
    host: process.env.DB_HOST || "",
    user: process.env.DB_USER || "",
    password: process.env.DB_PASSWORD || "",
    database: databaseName,
    port: parseInt(process.env.DB_PORT || "3306"),
    ssl: {
        ca: caCert,
    },
};

async function createUser(email: string | undefined, name: string | undefined, image: string | undefined) {
    try {
      if (!email) {
        throw new Error('Email not found in session');
      }
  
      const connection = await createConnection(dbConfig);
  
      try {
        const [users] = await connection.execute<RowDataPacket[]>(
          `SELECT * FROM users WHERE email = ?`,
          [email]
        );
  
        if (users.length === 0) {
          // User does not exist, add them with default tokens.
          await connection.execute(
            `INSERT INTO users (name, email, google_image_url, token_remaining, signup_date) VALUES (?, ?, ?, 5, NOW())`,
            [name, email, image]
          );
          console.log('User added with default tokens');
        } else {
          // User exists. Consider not updating tokens or handle other user-specific updates here.
          console.log('Existing user logged in');
        }
      } finally {
        await connection.end();
      }
    } catch (error) {
      console.error(error);
      throw error;
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
        async jwt({token, profile, session, user, account, trigger}) {
            if (trigger === "signIn" || trigger == "signUp") {
                if (trigger === "signIn") {
                    await createUser(profile?.email, profile?.name, user?.image || "")
                }
                if (token && profile) {
                    token.id = profile.sub
                } else if (token?.sub) {
                    token.id = token.sub
                }
            }
            return token
        },
        session: async ({session, token}) => {
            if (session?.user && !session.user.id) {
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