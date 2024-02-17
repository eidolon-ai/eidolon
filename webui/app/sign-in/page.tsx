// mark as client component
"use client";

// importing necessary functions
import {useSession} from "next-auth/react"

import {LoginButton} from '@/components/login-button'
import {redirect} from 'next/navigation'

export default function SignInPage() {
  const {data: session} = useSession()

  // redirect to home if user is already logged in
  if (session?.user) {
    redirect('/')
  }
  return (
    <div className="flex h-[calc(100vh-theme(spacing.16))] items-center justify-center py-10">
      <LoginButton/>
    </div>
  )
}
