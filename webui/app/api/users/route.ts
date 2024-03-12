'use server'
import { createConnection } from 'mysql2/promise';
import { config } from 'dotenv';
import {getServerSession, Session} from "next-auth";
import { RowDataPacket } from 'mysql2';
import { NextRequest, NextResponse } from 'next/server';

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

const caCert = process.env.CA_CERT;

// Configure the database connection
const dbConfig: DbConfig = {
        host: process.env.DB_HOST || "",
        user: process.env.DB_USER || "",
        password: process.env.DB_PASSWORD || "",
        database: process.env.DB_NAME || "",
        port: parseInt(process.env.DB_PORT || "3306"),
        ssl: {
            ca: caCert || "",
        },
    };




export async function POST(req: NextRequest, res: NextResponse) {
    try {
      const { email, name, image } = await req.json();
      await createUser(email, name, image);
    } catch (error) {
      console.error(error);
    }
  }

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



export async function GET(req: Request): Promise<Response> {
    console.log('GET request');
    try {
        const sesh = await getServerSession(); // Make sure to pass `req` if your session function needs it
        
        let email = sesh?.user?.email;
        if (!email) {
            return new Response(JSON.stringify({ error: 'User not authenticated' }), {
                status: 401, // Unauthorized
                headers: { 'Content-Type': 'application/json' },
            });
        }

        const connection = await createConnection(dbConfig);
        console.log('Connection established')
        const [users] = await connection.execute<RowDataPacket[]>(
            `SELECT token_remaining FROM users WHERE email = ?`,
            [email]
        );

        await connection.end();

        if (users.length > 0) {
            return new Response(JSON.stringify(users[0]), {
                status: 200,
                headers: { 'Content-Type': 'application/json' },
            });
        } else {
            return new Response(JSON.stringify({ error: 'User not found' }), {
                status: 404,
                headers: { 'Content-Type': 'application/json' },
            });
        }
    } catch (error) {
        console.error(error);
        return new Response(JSON.stringify({ error: 'Failed to fetch user data' }), {
            status: 500,
            headers: { 'Content-Type': 'application/json' },
        });
    }
}



export async function PUT(req: Request) {
    try {
        const sesh = await getServerSession(); 
        let email = null; // Default to null, adjust as needed

        if (sesh && sesh.user && sesh.user.email) {
            email = sesh.user.email;
        } else {
            // If session or user email is not found, return an error response
            return new Response(JSON.stringify({ error: 'User not authenticated or email not found' }), {
                status: 401, // Unauthorized
                headers: { 'Content-Type': 'application/json' },
            });
        }

        const connection = await createConnection(dbConfig);
        
        // First, fetch the current tokens remaining for the user
        const [rows] = await connection.execute<RowDataPacket[]>(
            `SELECT token_remaining FROM users WHERE email = ?`,
            [email]
        );

        if (rows.length > 0 && rows[0].token_remaining > 0) {
            // If tokens are available, subtract one and update the database
            await connection.execute(
                `UPDATE users SET token_remaining = token_remaining - 1 WHERE email = ? AND token_remaining > 0`,
                [email]
            );
            console.log('1 token subtracted successfully');
            await connection.end();
            return new Response(JSON.stringify({ message: '1 token subtracted successfully' }), {
                status: 200,
                headers: { 'Content-Type': 'application/json' },
            });
        } else {
            // If no tokens are remaining, return an error response
            await connection.end();
            return new Response(JSON.stringify({ error: 'No tokens remaining to subtract' }), {
                status: 400, // Bad Request
                headers: { 'Content-Type': 'application/json' },
            });
        }
    } catch (error) {
        console.error(error);
        return new Response(JSON.stringify({ error: 'Failed to subtract tokens' }), {
            status: 500,
            headers: { 'Content-Type': 'application/json' },
        });
    }
}
