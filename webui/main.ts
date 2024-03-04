const { createConnection } = require('mysql2/promise');

const { config } = require('dotenv');

// Load environment variables
config();

// Database configuration
const host = process.env.DB_HOST;
const user = process.env.DB_USER;
const password = process.env.DB_PASSWORD;
const database = process.env.DB_NAME;
const port = Number(process.env.DB_PORT || 3306);

async function testConnection() {
    try {
        const connection = await createConnection({
            host,
            user,
            password,
            database,
            port,
        });
        
        console.log("Connection successful.");
        
        // Close the connection
        await connection.end();
    } catch (error) {
        console.error("Connection failed:", error);
    }
}

testConnection();

