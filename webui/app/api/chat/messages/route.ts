'use server'

import {ChatEvent} from "@/lib/types";
import {getServerSession} from "next-auth";
import {authOptions} from "@/app/api/auth/[...nextauth]/route";
import {revalidatePath} from "next/cache";

const chatServerURL = process.env.EIDOLON_SERVER

const getUserId = (async () => (await getServerSession(authOptions))?.user?.id)

export async function POST(req: Request) {
  const params = await req.json()
  try {

    const response = await fetch(`${chatServerURL}${params.path}`, {
      method: "POST",
      body: JSON.stringify(params.data),
      headers: {
        'accept': 'text/event-stream',
        "Content-Type": "application/json"
      }
    })
    if (response.body) {
      const reader = response.body.getReader();
      const retStream = new ReadableStream({
        start: async (controller) => {
          try {
            while (true) {
              const {done, value} = await reader.read();
              if (done) break;
              controller.enqueue(value)
            }
          } finally {
            reader.releaseLock();
            controller.close();
          }
        },
        cancel: () => {
          reader.cancel("User cancelled request")
        }
      });

      let res = new Response(retStream);
      res.headers.set('Content-Type', 'text/event-stream')
      res.headers.set('Cache-Control', 'no-cache')
      res.headers.set('Connection', 'keep-alive')
      return res
    } else {
      return new Response('Failed to obtain stream', {status: 500})
    }
  } catch (error) {
    console.error('Error fetching SSE stream:', error);
    return new Response('Failed to obtain stream', {status: 500})
  }
}


export async function getChatEvents(agentName: string, processId: string) {
  revalidatePath(`${chatServerURL}/agents/${agentName}/processes/${processId}/events`)
  const userId = await getUserId()
  const results = await fetch(`${chatServerURL}/agents/${agentName}/processes/${processId}/events?userId=${userId}`)
    .then(resp => resp.json())

  const ret = []
  for (const json of results) {
    ret.push(json as ChatEvent)
  }

  return ret
}

