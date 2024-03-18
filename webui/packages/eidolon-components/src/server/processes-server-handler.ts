import {EidolonClient} from "@eidolon/client";

export const getAuthHeaders = (access_token: string | undefined): Record<string, string> => {
  if (!access_token) {
    return {} as Record<string, string>
  }
  return {
    "Authorization": `Bearer ${access_token}`
  }
}

async function getJsonOrEmpty(req: Request) {
  return await req.json().catch(() => ({"machineUrl": process.env.EIDOLON_MACHINE_URL || "http://localhost:8080"}))
}

export class ProcessesHandler {
  private readonly accessTokenFn: () => Promise<string | undefined>

  constructor(accessTokenFn: () => Promise<string | undefined>) {
    this.accessTokenFn = accessTokenFn
  }

  async GET(req: Request): Promise<Response> {
    let reqBody = await getJsonOrEmpty(req);
    const machineUrl = reqBody["machineUrl"]
    const client = new EidolonClient(machineUrl, getAuthHeaders(await this.accessTokenFn()))
    const resp = await client.getProcesses()
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
    const client = new EidolonClient(machineUrl, getAuthHeaders(await this.accessTokenFn()))
    const resp = await client.process(params.processid).status()

    return Response.json(resp)
  }

  async POST(req: Request): Promise<Response> {
    let reqBody = await req.json();
    const machineUrl = reqBody["machineUrl"]
    const title = reqBody["title"]
    const client = new EidolonClient(machineUrl, getAuthHeaders(await this.accessTokenFn()))
    const {status: resp} = await client.createProcess(title)

    return Response.json(resp)
  }

  async DELETE(req: Request, {params}: { params: { processid: string } }): Promise<Response> {
    let reqBody = await req.json();
    const machineUrl = reqBody["machineUrl"]
    const client = new EidolonClient(machineUrl, getAuthHeaders(await this.accessTokenFn()))
    const resp = await client.process(params.processid).delete()

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
    const client = new EidolonClient(machineUrl, getAuthHeaders(await this.accessTokenFn()))
    const resp = await client.process(params.processid).events()

    return Response.json(resp)
  }

  async POST(req: Request, {params}: { params: { processid: string } }) {
    try {
      const reqBody = await req.json()
      const {readable, writable} = new TransformStream();
      const writer = writable.getWriter();

      // Send an initial message
      let textEncoder = new TextEncoder();
      await writer.write(textEncoder.encode('data: Connected\n\n'));
      const machineUrl = reqBody["machineUrl"]
      const agent = reqBody["agent"]
      const operation = reqBody["operation"]
      const client = new EidolonClient(machineUrl, getAuthHeaders(await this.accessTokenFn()))
      const resp = client.process(params.processid).agent(agent).stream_action(operation, reqBody)
      for await (const event of resp) {
        await writer.write(textEncoder.encode(`data: ${JSON.stringify(event)}\n\n`));
      }

      // Clean up the interval when the client disconnects
      req.signal.onabort = () => {
        writer.close();
      };

      return new Response(readable, {
        status: 200,
        headers: {
          'Content-Type': 'text/event-stream',
          'Cache-Control': 'no-cache',
          'Connection': 'keep-alive',
        },
      });
    } catch (error) {
      console.error('Error fetching SSE stream:', error);
      return new Response('Failed to obtain stream', {status: 500})
    }
  }
}
