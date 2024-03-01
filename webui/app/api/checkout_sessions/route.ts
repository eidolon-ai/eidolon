import type {NextApiRequest, NextApiResponse} from 'next';
import Stripe from 'stripe';
import {redirect} from "next/navigation";
import { NextResponse } from 'next/server';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);
const baseURL = process.env.NEXTAUTH_URL;

export async function POST(req: NextApiRequest, res: NextApiResponse) {
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
      success_url: `${baseURL}/profile/?success=true`,
      cancel_url: `${baseURL}/profile/?canceled=true`,
      automatic_tax: {enabled: true},
    });
    console.log("stripe_after")
    // Redirect to the session URL
    console.log(res)
    console.log("*****session", session.url)
    return NextResponse.redirect(session.url!, 302);
  } catch (err) {
    // Make sure to return a response in case of error
    console.error('Error creating Stripe Session:', err);
    return new Response('Failed to create Stripe Session', {status: 500})
  }
}
