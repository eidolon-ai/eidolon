'use client';
import { useState, useEffect } from 'react';

export default function PreviewPage() {
  const [tokensRemaining, setTokensRemaining] = useState(null);

  // Define a function to fetch tokens remaining
  const fetchTokensRemaining = () => {
    fetch('/api/users', { // Make sure this endpoint is correct
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        // Include session token or credentials if required
      },
    })
    .then(response => response.json())
    .then(data => {
      if (data.token_remaining !== undefined) {
        setTokensRemaining(data.token_remaining);
      } else {
        console.error('Failed to fetch tokens remaining');
      }
    })
    .catch(error => console.error('Error fetching tokens remaining:', error));
  };

  // Fetch tokens remaining on component mount
  useEffect(() => {
    fetchTokensRemaining();

    // Initial checks for Stripe checkout feedback
    const query = new URLSearchParams(window.location.search);
    if (query.get('success')) {
      console.log('Order placed! You will receive an email confirmation.');
    }
    if (query.get('canceled')) {
      console.log('Order canceled -- continue to shop around and checkout when you’re ready.');
    }
  }, []);

  const updateUser = () => {
    fetch('/api/users', {
      method: 'PUT',
    })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      // Re-fetch tokens remaining to update the UI with the new count
      fetchTokensRemaining();
    })
    .catch(error => console.error('Error updating user:', error));
  };

  return (
    <div>
      {/* <button role="link" onClick={updateUser}>
          Subtract Token
      </button>  */}
      <p>Tokens remaining: {tokensRemaining}</p>
      <form action="/api/checkout_sessions" method="POST">
      <section>
          <p>Please ensure you enter your Gmail address exactly as registered, including any dots. Or the stripe payment will not associate the tokens with your account.</p>
          <button type="submit" role="link">
            Checkout
          </button>
        </section>
        <style jsx>{`
          section {
            background: #ffffff;
            display: flex;
            flex-direction: column;
            width: 400px;
            height: 112px;
            border-radius: 6px;
            justify-content: space-between;
          }
          button {
            height: 36px;
            background: #556cd6;
            border-radius: 4px;
            color: white;
            border: 0;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            box-shadow: 0px 4px 5.5px 0px rgba(0, 0, 0, 0.07);
          }
          button:hover {
            opacity: 0.8;
          }
        `}</style>
      </form>
    </div>
    
  );
}








