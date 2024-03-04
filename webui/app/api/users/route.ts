import { createConnection } from 'mysql2/promise';
import { config } from 'dotenv';
import {getServerSession} from "next-auth";
import { RowDataPacket } from 'mysql2';



// Load environment variables for database configuration
config();

// Database configuration
const dbConfig = {
    host: process.env.DB_HOST,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME,
    port: Number(process.env.DB_PORT || 3306),
};


  
  // Assuming sesh.user is of type User
export async function POST(req: Request): Promise<Response> {
    try {
        const sesh = await getServerSession(); // Make sure to pass `req` if your session function needs it
        let email: string | null = null; // Default to null, adjust as needed

        if (sesh && sesh.user && sesh.user.email) {
            email = sesh.user.email;
        }

        // Ensure email is present
        if (!email) {
            return new Response(JSON.stringify({ error: 'No email provided' }), {
                status: 400,
                headers: { 'Content-Type': 'application/json' },
            });
        }

        const connection = await createConnection(dbConfig);

        // First, check if the user already exists
        const [users] = await connection.execute<RowDataPacket[]>(
            `SELECT * FROM users WHERE email = ?`,
            [email]
        );

        // Now you can safely check users.length because TypeScript knows users is an array
        if (users.length === 0) {
            // User does not exist, add them with default tokens
            await connection.execute(
                `INSERT INTO users (name, email, google_image_url, token_remaining, signup_date) VALUES (?, ?, ?, 5, NOW())`,
                [sesh?.user?.name, email, sesh?.user?.image]
            );
            console.log('User added with default tokens');
        } else {
            // User exists, update their tokens
            await connection.execute(
                `UPDATE users SET token_remaining = token_remaining + 5 WHERE email = ?`,
                [email]
            );
            console.log('Tokens updated for existing user');
        }

        await connection.end();
        return new Response(JSON.stringify({ message: 'Operation successful' }), {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
        });
    } catch (error) {
        console.error(error);
        return new Response(JSON.stringify({ error: 'Failed to execute operation' }), {
            status: 500,
            headers: { 'Content-Type': 'application/json' },
        });
    }
}



export async function GET(req: Request): Promise<Response> {
    console.log('GET request');
    try {
        const sesh = await getServerSession(req); // Make sure to pass `req` if your session function needs it
        
        let email = sesh?.user?.email;
        if (!email) {
            return new Response(JSON.stringify({ error: 'User not authenticated' }), {
                status: 401, // Unauthorized
                headers: { 'Content-Type': 'application/json' },
            });
        }

        const connection = await createConnection(dbConfig);
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
