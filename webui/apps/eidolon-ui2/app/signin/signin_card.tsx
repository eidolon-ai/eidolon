'use client'

import React from 'react';
import { EidolonProvider } from "../../auth";
import SigninForm from "./SigninForm";
import { useSearchParams } from "next/navigation";
import Link from 'next/link';

export interface SigninProps {
  providers: Record<string, EidolonProvider[]>
  doSignin: (providerId: string, formData: FormData) => Promise<void>
}

const signinErrors: Record<string, string> = {
  default: "Unable to sign in.",
  Signin: "Try signing in with a different account.",
  OAuthSignin: "Try signing in with a different account.",
  OAuthCallbackError: "Try signing in with a different account.",
  OAuthCreateAccount: "Try signing in with a different account.",
  EmailCreateAccount: "Try signing in with a different account.",
  Callback: "Try signing in with a different account.",
  OAuthAccountNotLinked:
    "To confirm your identity, sign in with the same account you used originally.",
  EmailSignin: "The e-mail could not be sent.",
  CredentialsSignin:
    "Sign in failed. Check the details you provided are correct.",
  SessionRequired: "Please sign in to access this page.",
}

export default function SigninCard({ providers, doSignin }: SigninProps) {
  const params = useSearchParams()
  let error = undefined
  if (params.get("error")) {
    const errorValue = params.get("error")!
    error = signinErrors[errorValue] ?? signinErrors.default
  }

  return (
    <div className="bg-white shadow-lg rounded-lg p-8 max-w-md w-full">
      <h2 className="text-2xl font-bold text-center mb-4">
        Eidolon Demo Cloud
      </h2>
      {error && (
        <p className="text-red-500 mb-4">
          {error}
        </p>
      )}
      <div className="flex flex-col">
        {Object.keys(providers).map((providerType, index) => (
          <div key={providerType} className="flex flex-col">
            <div className="mb-2">
              {providers[providerType]!.map((provider) => (
                <SigninForm
                  key={provider.id}
                  provider={{
                    id: provider.id,
                    type: provider.type,
                    style: provider.style,
                    name: provider.name,
                    credentials: provider.credentials,
                  }}
                  doSignin={doSignin}
                />
              ))}
            </div>
            {index < Object.keys(providers).length - 1 && (
              <div className="relative flex py-5 items-center">
                <div className="flex-grow border-t border-gray-300"></div>
                <span className="flex-shrink mx-4 text-gray-400">or</span>
                <div className="flex-grow border-t border-gray-300"></div>
              </div>
            )}
          </div>
        ))}
      </div>
      <div className="border-t border-gray-300 my-4"></div>
      <p className="text-center text-sm text-gray-600 mt-4">
        By logging in, you agree to our{' '}
        <Link href="http://www.eidolonai.com/terms" className="text-blue-500 hover:underline">
          Terms of Service
        </Link>
      </p>
      <p className="text-center text-sm text-gray-600 mt-4">
        Have questions?{' '}
        <Link href="https://discord.gg/6kVQrHpeqG" className="text-blue-500 hover:underline">
          Visit us on Discord
        </Link>
      </p>
    </div>
  )
}