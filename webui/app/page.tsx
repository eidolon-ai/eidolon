import {getChats} from "@/app/api/chat/route";
import {redirect} from "next/navigation";

export const runtime = 'nodejs'

export default async function IndexPage() {
  const chats = await getChats().then(c => c.reverse())
  if (chats.length != 0) {
    redirect(`/chat/${chats[0].id}`)
  }
}
