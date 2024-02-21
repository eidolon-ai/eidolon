import {getChats} from "@/app/api/chat/route";
import {redirect} from "next/navigation";
import {getServerSession} from "next-auth";

export const runtime = 'nodejs'

export default async function IndexPage() {
  const session = await getServerSession()

  if (!session?.user) {
    redirect(`/sign-in?next=/`)
  }

  return (
    <img src="/background.png" alt="background" style={{height:"100%", opacity:.8}} />
  )
}
