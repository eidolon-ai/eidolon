import type {NextRequest, } from 'next/server';
import Stripe from 'stripe';
import {redirect} from "next/navigation";
import dotenv from 'dotenv';

dotenv.config();

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);
const baseURL = process.env.NEXTAUTH_URL;
const stripePriceId = process.env.STRIPE_PRICE_ID;
export async function POST(req: NextRequest, res: Response) {
  try {
    // Create Checkout Sessions from body params.
    console.log("stripe_before")
    const session = await stripe.checkout.sessions.create({
      line_items: [{
        // Provide the exact Price ID of the product you want to sell
        price: stripePriceId,
        quantity: 1,
      }],
      mode: 'payment',
      success_url: `${baseURL}/profile/?success=true`,
      cancel_url: `${baseURL}/profile/?canceled=true`,
      automatic_tax: {enabled: true},
    });
    console.log("stripe_after")
    // Redirect to the session URL
    console.log(res)
    console.log("*****session", session.url)
    return Response.redirect(session.url!, 302);
  } catch (err) {
    // Make sure to return a response in case of error
    console.error('Error creating Stripe Session:', err);
    return new Response('Failed to create Stripe Session', {status: 500})
  }
}
