import {getChats} from "@/app/api/chat/route";
import {Chat} from "@/lib/types";
import {redirect} from "next/navigation";

export const runtime = 'nodejs'

export default async function IndexPage() {
  const chats = await getChats().then(c => c.reverse())
  let chat: Chat
  if (chats.length == 0) {
    "here"
  } else {
    redirect(`/chat/${chats[0].id}`)
  }
}
