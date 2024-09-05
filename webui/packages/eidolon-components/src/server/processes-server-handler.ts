import {EidolonClient, HttpException} from "@eidolon-ai/client";

export async function processHeadersAndResponse(request: Request, promise: Promise<any>) {
  const realFetch = globalThis.fetch || fetch;
  /*global globalThis*/

  globalThis.fetch = function patchedFetch(uri, options) {
    if (request.headers) {
      const localHeaders = new Headers(request.headers || {})
      if (localHeaders.get('X-Eidolon-Context')) {
        const newHeaders: Record<string, string> = {}
        if (options?.headers) {
          Object.assign(newHeaders, options.headers)
        }
        const headersToFind = localHeaders.get('X-Eidolon-Context')?.split(",") || []
        headersToFind.forEach((header) => {
          const value = localHeaders.get(header)
          if (value) {
            newHeaders[header] = value
          }
        })
        newHeaders['X-Eidolon-Context'] = localHeaders.get('X-Eidolon-Context')!
        if (!options) {
          options = {}
        }
        options.headers = newHeaders
      }
    }
    return realFetch(uri, options);
  };
  return convertException(promise.then(Response.json)).finally(() => {
    globalThis.fetch = realFetch;
  })
}

export async function convertException(promise: Promise<any>) {
  return promise.catch((e) => {
    if (e instanceof HttpException) {
      return new Response(e.statusText, {status: e.status, statusText: e.statusText})
    } else if (e instanceof Error) {
      // @ts-ignore
      if (e?.cause?.code === 'ECONNREFUSED') {
        return new Response('Server Down', {status: 503})
      }

      return new Response(e.message, {status: 500})
    } else {
      if (e?.cause?.code === 'ECONNREFUSED') {
        return new Response('Server Down', {status: 503})
      }

      return new Response('Unknown error', {status: 500})
    }
  })
}


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
    return processHeadersAndResponse(req, this.getAgents(machineUrl))
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
    return processHeadersAndResponse(req, this.getOperations(machineUrl, params.agent))
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
    return processHeadersAndResponse(req, this.getProcesses(machineUrl))
  }

  async POST(req: Request): Promise<Response> {
    let reqBody = await req.json();
    const machineUrl = reqBody["machineUrl"]
    const agent = reqBody["agent"]
    const title = reqBody["title"]
    return processHeadersAndResponse(req, this.createProcess(machineUrl, agent, title))
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

    return processHeadersAndResponse(req, resp)
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
    return processHeadersAndResponse(req, this.deleteProcess(machineUrl, params.processid))
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
    return processHeadersAndResponse(req, this.getEvents(machineUrl, params.processid))
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
        let response = Response.json((await client.process(processId).agent(agent).action(operation, data))["data"], {status: 200});
        return response;
      }
    } catch (error) {
      console.error('Error fetching information:', error);
      return new Response('Failed to obtain stream', {status: 500})
    }
  }

  async* execOperation(machineUrl: string, processId: string, agent: string, operation: string, reqBody: Record<string, any>) {
    const client = new EidolonClient(machineUrl, getAuthHeaders(await this.accessTokenFn()))
    for await (const e of client.process(processId).agent(agent).stream_action(operation, reqBody)) {
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
    return processHeadersAndResponse(req, this.uploadFile(machineUrl, params.processid, await req.blob(), mimeType))
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
    return processHeadersAndResponse(req, this.setMetadata(machineUrl, params.processid, params.fileid, reqBody))
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
    return processHeadersAndResponse(req, this.deleteFile(machineUrl, params.processid, params.fileid).then(() => "ok"))
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
