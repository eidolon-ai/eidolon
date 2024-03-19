import {EidolonClient} from "@eidolon/client";

export const getAuthHeaders = (access_token: string | undefined): Record<string, string> => {
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
    const machineUrl = new URL(req.url).searchParams.get('machineURL')
    if (!machineUrl) {
      return new Response('machineUrl is required', {status: 400})
    }
    const resp = await this.getProcesses(machineUrl);
    return Response.json(resp)
  }

  async POST(req: Request): Promise<Response> {
    let reqBody = await req.json();
    const machineUrl = reqBody["machineUrl"]
    const agent = reqBody["agent"]
    const title = reqBody["title"]
    const resp = await this.createProcess(machineUrl, agent, title);

    return Response.json(resp)
  }

  async getProcesses(machineUrl: string) {
    const client = new EidolonClient(machineUrl, getAuthHeaders(await this.accessTokenFn()))
    return await client.getProcesses(0, 100);
  }

  async createProcess(machineUrl: string, agent: string, title: string) {
    const client = new EidolonClient(machineUrl, getAuthHeaders(await this.accessTokenFn()))
    const {status: resp} = await client.createProcess(agent, title)
    return resp;
  }
}


export class ProcessHandler {
  private readonly accessTokenFn: () => Promise<string | undefined>

  constructor(accessTokenFn: () => Promise<string | undefined>) {
    this.accessTokenFn = accessTokenFn
  }

  async GET(req: Request, {params}: { params: { processid: string } }): Promise<Response> {
    const machineUrl = new URL(req.url).searchParams.get('machineURL')
    if (!machineUrl) {
      return new Response('machineUrl is required', {status: 400})
    }
    let processId = params.processid;
    const resp = await this.getProcess(machineUrl, processId);

    return Response.json(resp)
  }

  async getProcess(machineUrl: string, processId: string) {
    const client = new EidolonClient(machineUrl, getAuthHeaders(await this.accessTokenFn()))
    return await client.process(processId).status();
  }

  async DELETE(req: Request, {params}: { params: { processid: string } }): Promise<Response> {
    const machineUrl = new URL(req.url).searchParams.get('machineURL')
    if (!machineUrl) {
      return new Response('machineUrl is required', {status: 400})
    }
    await this.deleteProcess(machineUrl, params.processid);

    return Response.json({status: "ok"})
  }

  async deleteProcess(machineUrl: string, processid: string) {
    const client = new EidolonClient(machineUrl, getAuthHeaders(await this.accessTokenFn()))
    return await client.process(processid).delete();
  }
}

export class ProcessEventsHandler {
  private readonly accessTokenFn: () => Promise<string | undefined>

  constructor(accessTokenFn: () => Promise<string | undefined>) {
    this.accessTokenFn = accessTokenFn
  }

  async GET(req: Request, {params}: { params: { processid: string } }): Promise<Response> {
    const machineUrl = new URL(req.url).searchParams.get('machineURL')
    if (!machineUrl) {
      return new Response('machineUrl is required', {status: 400})
    }
    const resp = await this.getEvents(machineUrl, params.processid);

    return Response.json(resp)
  }

  async getEvents(machineUrl: string, processid: string) {
    const client = new EidolonClient(machineUrl, getAuthHeaders(await this.accessTokenFn()))
    return await client.process(processid).events();
  }

  async POST(req: Request, {params}: { params: { processid: string } }) {
    try {
      const reqBody = await req.json()

      // Send an initial message
      let textEncoder = new TextEncoder();
      const machineUrl = reqBody["machineUrl"]
      const agent = reqBody["agent"]
      const operation = reqBody["operation"]
      const data = reqBody["data"] as Record<string, any>
      const processId = params.processid;
      let done = false;
      const retStream = new ReadableStream({
        start: async (controller) => {
          const resp = await this.execOperation(machineUrl, processId, agent, operation, data);
          for await (const event of resp) {
            if (done) break;
            controller.enqueue(textEncoder.encode(`data: ${JSON.stringify(event)}\n\n`));
          }
          controller.close()
        },
        cancel: () => {
        }
      });

      // Clean up the interval when the client disconnects
      req.signal.onabort = () => {
        done = true
      };

      return new Response(retStream, {
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

  async execOperation(machineUrl: string, processId: string, agent: string, operation: string, reqBody: Record<string, any>) {
    const client = new EidolonClient(machineUrl, getAuthHeaders(await this.accessTokenFn()))
    return client.process(processId).agent(agent).stream_action(operation, reqBody);
  }
}
