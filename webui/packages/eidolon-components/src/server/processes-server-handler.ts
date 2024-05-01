import {EidolonClient} from "@eidolon/client";
import {clearUsageCache} from "../usage-summary/usage_summary";
import {convertException, processResponse} from "../lib/util";

export const getAuthHeaders = (access_token: string | undefined): Record<string, string> => {
  if (!access_token) {
    return {} as Record<string, string>
  }
  return {
    "Authorization": `Bearer ${access_token}`
  }
}

export class MachineHandler {
  private readonly accessTokenFn: () => Promise<string | undefined>

  constructor(accessTokenFn: () => Promise<string | undefined>) {
    this.accessTokenFn = accessTokenFn
  }

  async GET(req: Request): Promise<Response> {
    const machineUrl = new URL(req.url).searchParams.get('machineURL')
    if (!machineUrl) {
      return new Response('machineUrl is required', {status: 422})
    }
    return processResponse(this.getAgents(machineUrl))
  }

  async getAgents(machineUrl: string) {
    const client = new EidolonClient(machineUrl, getAuthHeaders(await this.accessTokenFn()))
    return client.getAgents()
  }
}

export class AgentHandler {
  private readonly accessTokenFn: () => Promise<string | undefined>

  constructor(accessTokenFn: () => Promise<string | undefined>) {
    this.accessTokenFn = accessTokenFn
  }

  async GET(req: Request, {params}: { params: { agent: string } }): Promise<Response> {
    const machineUrl = new URL(req.url).searchParams.get('machineURL')
    if (!machineUrl) {
      return new Response('machineUrl is required', {status: 422})
    }
    return processResponse(this.getOperations(machineUrl, params.agent))
  }

  async getOperations(machineUrl: string, agent: string) {
    const client = new EidolonClient(machineUrl, getAuthHeaders(await this.accessTokenFn()))
    return client.getOperations(agent)
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
      return new Response('machineUrl is required', {status: 422})
    }
    return processResponse(this.getProcesses(machineUrl))
  }

  async POST(req: Request): Promise<Response> {
    let reqBody = await req.json();
    const machineUrl = reqBody["machineUrl"]
    const agent = reqBody["agent"]
    const title = reqBody["title"]
    return processResponse(this.createProcess(machineUrl, agent, title))
  }

  async getProcesses(machineUrl: string) {
    const client = new EidolonClient(machineUrl, getAuthHeaders(await this.accessTokenFn()))
    return client.getProcesses(0, 100)
  }

  async createProcess(machineUrl: string, agent: string, title: string) {
    const client = new EidolonClient(machineUrl, getAuthHeaders(await this.accessTokenFn()))
    return client.createProcess(agent, title).then((resp) => resp.status)
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
    const resp = this.getProcess(machineUrl, processId);

    return processResponse(resp)
  }

  async getProcess(machineUrl: string, processId: string) {
    console.debug('getting process with id', processId, 'from machine', machineUrl)
    const client = new EidolonClient(machineUrl, getAuthHeaders(await this.accessTokenFn()))
    return client.process(processId).status()
  }

  async DELETE(req: Request, {params}: { params: { processid: string } }): Promise<Response> {
    const machineUrl = new URL(req.url).searchParams.get('machineURL')
    if (!machineUrl) {
      return new Response('machineUrl is required', {status: 422})
    }
    return processResponse(this.deleteProcess(machineUrl, params.processid))
  }

  async deleteProcess(machineUrl: string, processid: string) {
    const client = new EidolonClient(machineUrl, getAuthHeaders(await this.accessTokenFn()))
    return client.process(processid).delete()
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
    return processResponse(this.getEvents(machineUrl, params.processid))
  }

  async getEvents(machineUrl: string, processid: string) {
    const client = new EidolonClient(machineUrl, getAuthHeaders(await this.accessTokenFn()))
    return client.process(processid).events()
  }

  async POST(req: Request, {params}: { params: { processid: string } }) {
    try {
      const reqBody = await req.json()

      const machineUrl = reqBody["machineUrl"]
      const agent = reqBody["agent"]
      const operation = reqBody["operation"]
      const data = reqBody["data"] as Record<string, any>

      const processId = params.processid;
      if (req.headers.get("Accept") === "text/event-stream") {
        let done = false;
        let textEncoder = new TextEncoder();
        const retStream = new ReadableStream({
          start: async (controller) => {
            const resp = this.execOperation(machineUrl, processId, agent, operation, data);
            for await (const event of resp) {
              await clearUsageCache()
              if (done) break;
              controller.enqueue(textEncoder.encode(`data: ${JSON.stringify(event)}\n\n`));
            }
            await clearUsageCache()
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
        return processResponse(client.process(processId).agent(agent).action(operation, data).then((resp) => {
          clearUsageCache()
          return resp.data
        }));
      }
    } catch (error) {
      console.error('Error fetching information:', error);
      await clearUsageCache()
      return new Response('Failed to obtain stream', {status: 500})
    }
  }

  async* execOperation(machineUrl: string, processId: string, agent: string, operation: string, reqBody: Record<string, any>) {
    const client = new EidolonClient(machineUrl, getAuthHeaders(await this.accessTokenFn()))
    for await (const e of client.process(processId).agent(agent).stream_action(operation, reqBody)) {
      await clearUsageCache()
      yield e
    }
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
    return processResponse(this.uploadFile(machineUrl, params.processid, await req.blob(), mimeType))
  }

  async uploadFile(machineUrl: string, processId: string, file: Blob, mimeType: string | null) {
    const client = new EidolonClient(machineUrl, getAuthHeaders(await this.accessTokenFn()))
    return client.process(processId).upload_file(file, mimeType)
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
    return processResponse(this.setMetadata(machineUrl, params.processid, params.fileid, reqBody))
  }

  // download file
  async GET(req: Request, {params}: { params: { processid: string, fileid: string } }) {
    const machineUrl = new URL(req.url).searchParams.get('machineURL')
    if (!machineUrl) {
      return new Response('machineUrl is required', {status: 400})
    }
    return convertException(this.downloadFile(machineUrl, params.processid, params.fileid).then(resp => {
      const {data, mimetype} = resp
      return new Response(data, {
        status: 200,
        headers: {
          'Content-Type': mimetype || 'application/octet-stream',
        },
      });
    }))
  }

  async DELETE(req: Request, {params}: { params: { processid: string, fileid: string } }) {
    const machineUrl = new URL(req.url).searchParams.get('machineURL')
    if (!machineUrl) {
      return new Response('machineUrl is required', {status: 400})
    }
    return processResponse(this.deleteFile(machineUrl, params.processid, params.fileid).then(() => "ok"))
  }

  async downloadFile(machineUrl: string, processId: string, fileId: string) {
    const client = new EidolonClient(machineUrl, getAuthHeaders(await this.accessTokenFn()))
    return client.process(processId).download_file(fileId)
  }

  async deleteFile(machineUrl: string, processId: string, fileId: string) {
    const client = new EidolonClient(machineUrl, getAuthHeaders(await this.accessTokenFn()))
    return client.process(processId).delete_file(fileId)
  }

  async setMetadata(machineUrl: string, processId: string, fileId: string, metadata: Record<string, any>) {
    const client = new EidolonClient(machineUrl, getAuthHeaders(await this.accessTokenFn()))
    return client.process(processId).set_metadata(fileId, metadata)
  }
}
