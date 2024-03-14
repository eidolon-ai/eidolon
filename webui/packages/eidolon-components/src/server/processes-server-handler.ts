import {ProcessStatus} from "../lib/types.js";
import {ChatEvent, ProcessState} from "@repo/eidolon-client/client";

export namespace ServerHandler {
  export const getAuthHeaders = async (access_token: string | undefined): Promise<Record<string, string>> => {
    if (!access_token) {
      return {} as Record<string, string>
    }
    return {
      "Authorization": `Bearer ${access_token}`
    }
  }

  export class ProcessesHandler {
    private readonly accessTokenFn: () => Promise<string | undefined>

    constructor(accessTokenFn: () => Promise<string | undefined>) {
      this.accessTokenFn = accessTokenFn
    }

    async GET(req: Request): Promise<Response> {
      let reqBody = await req.json();
      const machineUrl = reqBody["machineUrl"]
      let accessToken = await this.accessTokenFn();
      const resp = await getProcesses(accessToken, machineUrl)

      return Response.json(resp)
    }
  }


  export class ProcessHandler {
    private readonly accessTokenFn: () => Promise<string | undefined>

    constructor(accessTokenFn: () => Promise<string | undefined>) {
      this.accessTokenFn = accessTokenFn
    }

    async GET(req: Request, {params}: { params: { processid: string } }): Promise<Response> {
      let reqBody = await req.json();
      const machineUrl = reqBody["machineUrl"]
      let accessToken = await this.accessTokenFn();
      const resp = await getProcess(accessToken, machineUrl, params.processid)

      return Response.json(resp)
    }

    async POST(req: Request): Promise<Response> {
      let reqBody = await req.json();
      const machineUrl = reqBody["machineUrl"]
      const title = reqBody["title"]
      let accessToken = await this.accessTokenFn();
      const resp = await createProcess(accessToken, machineUrl, title)

      return Response.json(resp)
    }

    async DELETE(req: Request, {params}: { params: { processid: string } }): Promise<Response> {
      let reqBody = await req.json();
      const machineUrl = reqBody["machineUrl"]
      let accessToken = await this.accessTokenFn();
      const resp = await deleteProcess(accessToken, machineUrl, params.processid)

      return Response.json(resp)
    }
  }

  export class ProcessEventsHandler {
    private readonly accessTokenFn: () => Promise<string | undefined>

    constructor(accessTokenFn: () => Promise<string | undefined>) {
      this.accessTokenFn = accessTokenFn
    }

    async GET(req: Request, {params}: { params: { processid: string } }): Promise<Response> {
      let reqBody = await req.json();
      const machineUrl = reqBody["machineUrl"]
      let accessToken = await this.accessTokenFn();
      const resp = await getProcessEvents(accessToken, machineUrl, params.processid)

      return Response.json(resp)
    }

    async POST(req: Request, {params}: { params: { processid: string } }) {
      const reqBody = await req.json()
      try {
      let accessToken = await this.accessTokenFn();
        const machineUrl = reqBody["machineUrl"]
        const agent = reqBody["agent"]
        const operation = reqBody["operation"]
        const auth_headers = await getAuthHeaders(accessToken)
        const path = `${machineUrl}/processes/${params.processid}/${agent}/${operation}`
        const response = await fetch(path, {
          method: "POST",
          body: JSON.stringify(reqBody.data),
          headers: {
            "accept": "text/event-stream",
            "Content-Type": "application/json",
            ...auth_headers
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
  }

  /**
   * This function is to be mounted under the /api/eidolon/process route as a GET handler.
   *
   * This function should be hooked up like so:
   * ```ts
   * export const GET = async (req: Request): Promise<Response> => {
   *   const session = await getSession()
   *   const machineUrl = (await req.json())["machineUrl"]
   *   const resp = await ServerHandler.getProcessesHandler(machineUrl, session?.user?.access_token)
   *
   *   return Response.json(resp)
   * }
   * ```
   * @param machineURL the URL of the eidolon machine
   * @param access_token the access token of the user
   */
  export async function getProcesses(access_token: string | undefined, machineURL: string) {
    const auth_headers = await getAuthHeaders(access_token)
    const results = await fetch(`${machineURL}/system/processes`,
      {
        // @ts-ignore
        next: {tags: ['chats']},
        headers: auth_headers,
        method: 'GET',
        json: {machine: machineURL}
      }
    ).then(resp => {
      if (resp.status === 401) {
        console.log('Unauthenticated! Status: 401');
        return [];
      } else if (!resp.ok) {
        throw new Error(`HTTP error! status: ${resp.status}`);
      }
      return resp.json();
    })

    const ret = []
    for (const json of results) {
      json.id = json.process_id
      json.title = json.title || json.agent
      json.path = `/chat/${json.id}`
      ret.push(json as ProcessStatus)
    }

    return ret
  }

  export async function getProcess(access_token: string | undefined, machineURL: string, process_id: string) {
    const auth_headers = await getAuthHeaders(access_token)
    return fetch(`${machineURL}/system/processes/${process_id}/status`, {headers: auth_headers})
      .then(resp => {
        if (resp.status === 404) {
          return null
        }
        return resp.json().then((json: Record<string, any>) => json as ProcessState)
      })
  }

  /**
   * Create a new process. Make sure you invalidate the tag `chats` after calling this function
   * @param access_token
   * @param title
   */
  export async function createProcess(access_token: string | undefined, machineURL: string, title: string) {
    const auth_headers = await getAuthHeaders(access_token)
    const body = {title: title}
    const results = await fetch(`${machineURL}/system/processes`, {
      method: "POST",
      body: JSON.stringify(body),
      headers: {
        "Content-Type": "application/json",
        ...auth_headers
      }
    })

    return results.json()
  }

  export async function deleteProcess(access_token: string | undefined, machineURL: string, process_id: string) {
    const auth_headers = await getAuthHeaders(access_token)
    await fetch(`${machineURL}/system/processes/${process_id}`, {
      method: "DELETE",
      headers: auth_headers
    })
  }


  export async function getProcessEvents(access_token: string | undefined, machineURL: string, processId: string) {
    const auth_headers = await getAuthHeaders(access_token)
    const results = await fetch(`${machineURL}/system/processes/${processId}/events`, {headers: auth_headers})
      .then(resp => resp.json())

    const ret = []
    for (const json of results) {
      ret.push(json as ChatEvent)
    }

    return ret
  }
}
