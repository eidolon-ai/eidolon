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
      console.log('non existent machine url')
      return new Response('machineUrl is required', {status: 422})
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
    console.debug('listing processes from machine', machineUrl)
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
      console.error('machineUrl is required')
      return new Response('machineUrl is required', {status: 422})
    }
    let processId = params.processid;
    if (!processId) {
      console.error('params.processid is required')
      return new Response('params.processid is required', {status: 422})
    }
    const resp = await this.getProcess(machineUrl, processId);

    return Response.json(resp)
  }

  async getProcess(machineUrl: string, processId: string) {
    console.debug('getting process with id', processId, 'from machine', machineUrl)
    const client = new EidolonClient(machineUrl, getAuthHeaders(await this.accessTokenFn()))
    return await client.process(processId).status();
  }

  async DELETE(req: Request, {params}: { params: { processid: string } }): Promise<Response> {
    const machineUrl = new URL(req.url).searchParams.get('machineURL')
    if (!machineUrl) {
      return new Response('machineUrl is required', {status: 422})
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
      return new Response('machineUrl is required', {status: 422})
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

      const machineUrl = reqBody["machineUrl"]
      const agent = reqBody["agent"]
      const operation = reqBody["operation"]
      const data = reqBody["data"] as Record<string, any>
    console.log("*** data", data)

      const processId = params.processid;
      if (req.headers.get("Accept") === "text/event-stream") {
        let done = false;
        let textEncoder = new TextEncoder();
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
      } else {
        const client = new EidolonClient(machineUrl, getAuthHeaders(await this.accessTokenFn()))
        return Response.json((await client.process(processId).agent(agent).action(operation, data))["data"], {status: 200});
      }
    } catch (error) {
      console.error('Error fetching information:', error);
      return new Response('Failed to obtain stream', {status: 500})
    }
  }

  async execOperation(machineUrl: string, processId: string, agent: string, operation: string, reqBody: Record<string, any>) {
    const client = new EidolonClient(machineUrl, getAuthHeaders(await this.accessTokenFn()))
    return client.process(processId).agent(agent).stream_action(operation, reqBody);
  }
}

export class FilesHandler {
  private readonly accessTokenFn: () => Promise<string | undefined>

  constructor(accessTokenFn: () => Promise<string | undefined>) {
    this.accessTokenFn = accessTokenFn
  }

  // upload file
  async POST(req: Request, {params}: { params: { processid: string } }) {
    const machineUrl = new URL(req.url).searchParams.get('machineURL')
    if (!machineUrl) {
      return new Response('machineUrl is required', {status: 422})
    }
    const mimeType = req.headers.get('mime-type')
    let fileHandle = await this.uploadFile(machineUrl, params.processid, await req.blob(), mimeType);
    return Response.json(fileHandle);
  }

  async uploadFile(machineUrl: string, processId: string, file: Blob, mimeType: string | null) {
    const client = new EidolonClient(machineUrl, getAuthHeaders(await this.accessTokenFn()))
    return await client.process(processId).upload_file(file, mimeType);
  }
}

export class FileHandler {
  private readonly accessTokenFn: () => Promise<string | undefined>

  constructor(accessTokenFn: () => Promise<string | undefined>) {
    this.accessTokenFn = accessTokenFn
  }

  async POST(req: Request, {params}: { params: { processid: string, fileid: string } }) {
    const machineUrl = new URL(req.url).searchParams.get('machineURL')
    if (!machineUrl) {
      return new Response('machineUrl is required', {status: 400})
    }
    const reqBody = await req.json()
    const fileHandle = await this.setMetadata(machineUrl, params.processid, params.fileid, reqBody);
    return Response.json(fileHandle);
  }

  // download file
  async GET(req: Request, {params}: { params: { processid: string, fileid: string } }) {
    const machineUrl = new URL(req.url).searchParams.get('machineURL')
    if (!machineUrl) {
      return new Response('machineUrl is required', {status: 400})
    }
    let data = await this.downloadFile(machineUrl, params.processid, params.fileid);
    return new Response(data, {
        status: 200,
        headers: {
          'Content-Type': 'application/octet-stream',
        },
      });
  }

  async DELETE(req: Request, {params}: { params: { processid: string, fileid: string } }) {
    const machineUrl = new URL(req.url).searchParams.get('machineURL')
    if (!machineUrl) {
      return new Response('machineUrl is required', {status: 400})
    }
    await this.deleteFile(machineUrl, params.processid, params.fileid);
    return Response.json({status: "ok"});
  }

  async downloadFile(machineUrl: string, processId: string, fileId: string) {
    const client = new EidolonClient(machineUrl, getAuthHeaders(await this.accessTokenFn()))
    return await client.process(processId).download_file(fileId);
  }

  async deleteFile(machineUrl: string, processId: string, fileId: string) {
    const client = new EidolonClient(machineUrl, getAuthHeaders(await this.accessTokenFn()))
    return await client.process(processId).delete_file(fileId);
  }

  async setMetadata(machineUrl: string, processId: string, fileId: string, metadata: Record<string, any>) {
    const client = new EidolonClient(machineUrl, getAuthHeaders(await this.accessTokenFn()))
    return await client.process(processId).set_metadata(fileId, metadata);
  }
}
