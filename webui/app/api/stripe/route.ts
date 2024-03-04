import express, { Request, Response } from 'express';
import { createConnection } from 'mysql2/promise';
import dotenv from 'dotenv';

dotenv.config();

const STRIPE_SECRET_KEY = process.env.STRIPE_SECRET_KEY;
if (!STRIPE_SECRET_KEY) {
    throw new Error('The STRIPE_SECRET_KEY environment variable is not set.');
}

const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);
const app = express();

const endpointSecret = process.env.STRIPE_ENDPOINT_SECRET;

if (!endpointSecret) {
    throw new Error('The STRIPE_ENDPOINT_SECRET environment variable is not set.');
}

// Database configuration
const dbConfig = {
    host: process.env.DB_HOST,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME,
    port: Number(process.env.DB_PORT || 3306),
};

app.post('/webhook', express.raw({type: 'application/json'}), async (request: Request, response: Response) => {
    const sig = request.headers['stripe-signature'];

    let event;

    try {
        event = stripe.webhooks.constructEvent(request.body, sig, endpointSecret);
    } catch (err) {
        const error = err as Error;
        console.error(`Webhook Error: ${error.message}`);
        return response.status(400).send(`Webhook Error: ${error.message}`);
    }
    

    if (event.type === 'payment_intent.succeeded') {
        const paymentIntent = event.data.object; // The payment intent that succeeded
        // Assume customer email is stored in metadata or there's a way to identify the user
        const userEmail = paymentIntent.charges.data[0].billing_details.email;

        try {
            const connection = await createConnection(dbConfig);
            await connection.execute(
                `UPDATE users SET token_remaining = token_remaining + 5 WHERE email = ?`,
                [userEmail]
            );
            await connection.end();
            console.log(`Added 5 tokens for user ${userEmail}`);
        } catch (error) {
            console.error('Failed to update user tokens:', error);
            return response.status(500).send('Failed to update user tokens');
        }
    } else {
        console.log(`Unhandled event type ${event.type}`);
    }

    response.json({ received: true });
});

const port = process.env.PORT || 4242;
app.listen(port, () => console.log(`Webhook listener running on port ${port}`));
