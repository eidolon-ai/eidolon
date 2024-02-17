import {notFound, redirect} from 'next/navigation'

import {getChat} from "@/app/api/chat/route";
import * as React from "react";
import {getServerSession} from "next-auth";
import {ChatEvents} from "@/components/chat-events";

export const runtime = 'nodejs'
export const preferredRegion = 'home'

export interface ChatPageProps {
  params: {
    id: string
  }
}

export default async function ChatPage({params}: ChatPageProps) {
  const session = await getServerSession()

  if (!session?.user) {
    redirect(`/sign-in?next=/chat/${params.id}`)
  }

  const chat = await getChat(params.id)

  if (!chat) {
    notFound()
  }

  // @ts-ignore
  return (
    <ChatEvents agentName={chat.agent} processId={chat.process_id}/>
  )
}
