import type { NextApiRequest, NextApiResponse } from 'next';

const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

export async function POST(req: NextApiRequest, res: NextApiResponse) {
    if (req.method === 'POST') {
        try {
            // Create Checkout Sessions from body params.
            console.log("stripe_before")
            const session = await stripe.checkout.sessions.create({
                line_items: [{
                    // Provide the exact Price ID of the product you want to sell
                    price: 'price_1OoGyiGBK4zTc9Yyi2Nk52on',
                    quantity: 1,
                }],
                mode: 'payment',
                success_url: `http://localhost:3000/profile/?success=true`,
                cancel_url: `http://localhost:3000/profile/?canceled=true`,
                automatic_tax: { enabled: true },
            });
            console.log("stripe_after")
            // Redirect to the session URL
            console.log(res)
            return res.redirect(303, session.url);
        } catch (err) {
            // Make sure to return a response in case of error
            console.error('Error creating Stripe Session:', err);
            return new Response('Failed to create Stripe Session', {status: 500})
        }
    } else {
        // Handle any non-POST requests
        return res.setHeader('Allow', ['POST']).status(405).end(`Method ${req.method} Not Allowed`);
    }
}
