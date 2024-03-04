import { createConnection } from 'mysql2/promise';
import { config } from 'dotenv';
import {getServerSession} from "next-auth";


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

// export async function POST(req: Request) {
//     try {
//         const connection = await createConnection(dbConfig);
//         const { google_id } = await req.json(); // Assuming google_id is used to identify the user
//         await connection.execute(
//             `UPDATE users SET token_remaining = token_remaining + 5 WHERE google_id = ?`,
//             [google_id]
//         );
//         await connection.end();
//         return new Response(JSON.stringify({ message: '5 tokens added successfully' }), {
//             status: 200,
//             headers: { 'Content-Type': 'application/json' },
//         });
//     } catch (error) {
//         return new Response(JSON.stringify({ error: 'Failed to add tokens' }), {
//             status: 500,
//             headers: { 'Content-Type': 'application/json' },
//         });
//     }
// }


export async function GET(req: Request) {
    // Example: Fetch all users
    try {
        const connection = await createConnection(dbConfig);
        const [rows] = await connection.query(`SELECT * FROM users`);
        await connection.end();
        return new Response(JSON.stringify(rows), {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
        });
    } catch (error) {
        return new Response(JSON.stringify({ error: 'Failed to fetch users' }), {
            status: 500,
            headers: { 'Content-Type': 'application/json' },
        });
    }
}

export async function POST(req: Request) {
    const sesh = await getServerSession();
    let email = null; // Default to null, adjust as needed
    if (sesh && sesh.user) {
        email = sesh.user.email;
        }

    try {
        const connection = await createConnection(dbConfig);
        await connection.execute(
            `UPDATE users SET token_remaining = token_remaining - 1 WHERE email = ?`,
            [email]
        );
        console.log('query executed')
        await connection.end();
        return new Response(JSON.stringify({ message: '1 token subtracted successfully' }), {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
        });
    } catch (error) {
        return new Response(JSON.stringify({ error: 'Failed to subtract tokens' }), {
            status: 500,
            headers: { 'Content-Type': 'application/json' },
        });
    }
}