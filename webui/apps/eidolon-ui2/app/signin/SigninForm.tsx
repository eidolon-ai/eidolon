'use client'

import React from 'react';
import Image from 'next/image';

export interface SigninFormData {
  doSignin: (providerId: string, formData: FormData) => Promise<void>
  provider: any
}

export default function SigninForm({ provider, doSignin }: SigninFormData) {
  const csrfToken = "csrfToken"
  const providerLogoPath = "https://authjs.dev/img/providers"

  async function handleSubmit(providerId: string, event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const form = event.currentTarget
    const formData = new FormData(form)
    await doSignin(providerId, formData)
  }

  let bg, brandColor, logo
  if (provider.type === "oauth" || provider.type === "oidc") {
    bg = provider.style?.bg || "#fff"
    brandColor = provider.style?.brandColor
    logo = provider.style?.logo ?? `${providerLogoPath}/${provider.id}.svg`
  }
  let credentials = provider.credentials
  if (provider.type === "email") {
    credentials = {
      email: {
        label: "Email",
        type: "email",
        placeholder: "email@example.com"
      }
    }
  }

  const color = brandColor ?? bg ?? "#fff"

  return (
    <form onSubmit={(e) => handleSubmit(provider.id, e)} method="POST" className="w-full">
      <div key={provider.id} className="flex items-center justify-center m-2 w-full">
        {(provider.type === "oauth" || provider.type === "oidc") && (
          <button
            type="submit"
            className="flex items-center justify-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            <Image
              alt="provider-logo"
              src={logo}
              width={24}
              height={24}
              className="mr-2"
            />
            <span className="normal-case">Sign in with {provider.name}</span>
          </button>
        )}

        {(provider.type === "credentials" || provider.type === "email") && (
          <div className="flex flex-col w-full items-end">
            <div className="flex flex-col w-full">
              <input type="hidden" name="csrfToken" value={csrfToken} />
              {Object.keys(credentials).map((credential) => (
                <div key={credential} className="mb-4">
                  <label htmlFor={`input-${credential}-for-${provider.id}-provider`} className="block text-sm font-medium text-gray-700">
                    {credentials[credential].label ?? credential}
                  </label>
                  <input
                    id={`input-${credential}-for-${provider.id}-provider`}
                    name={credential}
                    type={credentials[credential].type ?? "email"}
                    required
                    className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                    placeholder={credentials[credential].placeholder ?? ""}
                  />
                </div>
              ))}
            </div>
            <button
              id="submitButton"
              type="submit"
              className="mt-4 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              <span className="normal-case">Sign in</span>
            </button>
          </div>
        )}

        {provider.type === "webauthn" && (
          <div>
            <input type="hidden" name="csrfToken" value={csrfToken} />
            {Object.keys(provider.formFields).map((field) => (
              <div key={`input-group-${provider.id}`} className="mb-4">
                <label
                  className="block text-sm font-medium text-gray-700"
                  htmlFor={`input-${field}-for-${provider.id}-provider`}
                >
                  {provider.formFields[field].label ?? field}
                </label>
                <input
                  name={field}
                  data-form-field
                  id={`input-${field}-for-${provider.id}-provider`}
                  type={provider.formFields[field].type ?? "email"}
                  placeholder={provider.formFields[field].placeholder ?? ""}
                  className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                  {...provider.formFields[field]}
                />
              </div>
            ))}
            <button
              id={`submitButton-${provider.id}`}
              type="submit"
              className="w-full inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Sign in with {provider.name}
            </button>
          </div>
        )}
      </div>
    </form>
  )
}