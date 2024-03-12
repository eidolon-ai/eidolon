// Assuming all necessary imports are at the top of the file
import { createConnection } from 'mysql2/promise';
import Stripe from 'stripe';
import { buffer } from "micro"; // If needed based on how you process the request body
import dotenv from 'dotenv';


dotenv.config();
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
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: "2023-10-16",
});

const webhookSecret = process.env.STRIPE_ENDPOINT_SECRET;

// This is a rough sketch; adjust types and implementations as needed
export async function POST(req: Request): Promise<Response> {
    console.log('POST request');
    const sig = req.headers.get('stripe-signature');

    let rawBody = await req.text(); // Assuming you can directly get the raw body from the Request

    try {
        const stripeEvent = stripe.webhooks.constructEvent(rawBody, sig!, webhookSecret!);
            // const test = stripeEvent.data.object as any
            // console.log(test)
            if (stripeEvent.type === 'charge.succeeded') {
                const charge = stripeEvent.data.object as Stripe.Charge;
                const userEmail = charge.billing_details.email;
            console.log(`Payment intent succeeded for user ${userEmail}`);

            if (userEmail) {

                const connection = await createConnection(dbConfig);
                console.log(`Connected to database for user ${userEmail}`);
                await connection.execute(
                    `UPDATE users SET token_remaining = token_remaining + 5 WHERE email = ?`,
                    [userEmail]
                );
                await connection.end();
                console.log(`Added 5 tokens for user ${userEmail}`);
            } else {
                console.log('Email address not found in payment intent charges.');
            }
        } else {
            console.log(`Unhandled event type ${stripeEvent.type}`);
        }

        return new Response(JSON.stringify({ received: true }), {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
        });
    } catch (err) {
        console.error(`Webhook Error: ${err}`);
        return new Response(JSON.stringify({ error: `Webhook Error: ${err}` }), {
            status: 400,
            headers: { 'Content-Type': 'application/json' },
        });
    }
}
