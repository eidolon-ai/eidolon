import {OpenAPIV3_1} from "openapi-types";
import {createParser, ParsedEvent, ParseEvent} from "eventsource-parser";
import {HttpException} from "./exceptions";

// Disable SSR for @readme/openapi-parser due to Turbopack incompatibility
const initializeParser = async () => {
  return (await import("@readme/openapi-parser")).default;
};

export interface ChatEvent extends Record<string, any> {
  event_type: string,
  category: string,
}

export interface OperationInfo {
  label: string
  machine: string
  agent: string
  name: string
  path: string
  summary?: string
  description?: string
  schema: OpenAPIV3_1.SchemaObject
}

export interface ProcessStatus {
  created: string
  updated: string
  machine: string,
  agent: string,
  process_id: string,
  title?: string,
  state: string,
  available_actions: string[]
  parent_process_id?: string
  error?: string
}

export interface ProcessStatusWithData extends ProcessStatus {
  data: any
}

export interface ProcessesResponse {
  processes: ProcessStatus[]
  total: number
  next?: string
}

export interface FileHandle {
  machineUrl: string
  processId: string
  fileId: string
  metadata?: Record<string, any>
}

function addMachineIfMissing(machineURL: string, process: ProcessStatus) {
  // @ts-ignore
  if (process['error_info'] == null) {
    // @ts-ignore
    delete process['error_info']
  }
  // @ts-ignore
  delete process['metadata']
  if (!process.machine) {
    process.machine = machineURL
  }
}

export class EidolonClient {
  private readonly machineUrl: string
  private isLoaded = false

  private actions: Record<string, OperationInfo> = {}
  private agents: string[] = []

  private readonly headers: Record<string, string>

  constructor(machineUrl: string, headers: Record<string, string> = {}) {
    this.machineUrl = machineUrl
    this.headers = {
      "Content-Type": "application/json",
      ...headers
    }
  }

  private processRequestBody(agent: string, name: string, path: string, requestBody: any) {
    const ret = {
      label: `${agent}:${name}`,
      machine: this.machineUrl,
      agent: agent,
      name: name,
      path: path,
      summary: requestBody?.summary,
      description: requestBody?.description,
      schema: {}
    } as OperationInfo

    if (requestBody?.content) {
      if ("application/json" in requestBody.content) {
        ret.schema = requestBody.content["application/json"].schema
      } else if ("multipart/form-data" in requestBody.content) {
        ret.schema = requestBody.content["multipart/form-data"].schema
      } else if ("text/plain" in requestBody.content) {
        ret.schema = requestBody.content["text/plain"].schema
      }
    }
    return ret
  }

  private async initialize() {
    if (!this.isLoaded) {
      const OpenAPIParser = await initializeParser();
      const results = await fetch(`${this.machineUrl}/openapi.json`, {headers: this.headers})
      if (results.status !== 200) {
        throw new HttpException(`Failed to fetch openapi.json: ${results.statusText}`, results.status)
      }
      const response = await results.json()
      const api = await OpenAPIParser.validate(response) as OpenAPIV3_1.Document
      const paths = api.paths!
      const agentRE = /\/agent\/([^/]+)/
      const agents = new Set<string>()
      for (const path in paths) {
        if (paths[path]?.post) {
          const requestBody = paths[path]!.post!.requestBody
          let agentREExec = agentRE.exec(path);
          if (agentREExec) {
            const agentName = agentREExec![1]!
            agents.add(agentName)
            let opName = path.substring(path.lastIndexOf('/') + 1);
            if (path.includes("process")) {
              this.actions[agentName + "-" + opName] = this.processRequestBody(agentName, opName, path, requestBody)
            }
          }
        }
      }
      this.agents = Array.from(agents).sort()
      this.isLoaded = true
    }
  }

  public async getActions() {
    await this.initialize()
    return this.actions
  }

  public async getAction(agentName: string, operationName: string) {
    await this.initialize()
    return this.actions[agentName + "-" + operationName]
  }

  public async getAgents() {
    await this.initialize()
    return this.agents
  }

  private convertBinary = (obj: any) => {
    if (!obj) {
      return
    }
    if (typeof obj === 'object') {
      if (obj['type'] === 'string' && obj['format'] === 'binary') {
        obj.format = 'data-url'
      } else {
        for (const key in obj) {
          this.convertBinary(obj[key])
        }
      }
    } else if (Array.isArray(obj)) {
      for (const item of obj) {
        this.convertBinary(item)
      }
    }
  }

  public async getOperations(agent: string): Promise<OperationInfo[]> {
    const ret = Object.values(await this.getActions())
      .filter(op => op.agent === agent)
      .sort((a, b) => a.label.localeCompare(b.label))
    for (const op of ret) {
      this.convertBinary(op.schema)
    }
    return ret
  }

  public async getProcesses(skip: number = 0, limit: number = 10) {
    const results = await fetch(`${this.machineUrl}/processes?skip=${skip}&limit=${limit}`, {headers: this.headers})
    if (results.status !== 200) {
      throw new HttpException(`Failed to fetch processes: ${results.statusText}`, results.status)
    }

    const response = await results.json() as ProcessesResponse
    if (response?.processes) {
      for (const process of response.processes) {
        addMachineIfMissing(this.machineUrl, process)
      }
    }
    return response
  }

  public async createProcess(agent: string, title: string | undefined = "") {
    const results = await fetch(`${this.machineUrl}/processes`, {
      headers: this.headers,
      method: 'POST',
      body: JSON.stringify({agent: agent, title: title})
    })
    if (results.status !== 200) {
      throw new HttpException(`Failed to create process: ${results.statusText}`, results.status)
    }
    let status = await results.json() as ProcessStatus;
    addMachineIfMissing(this.machineUrl, status)
    return {process: this.process(status.process_id), status: status}
  }

  public process(process_id: string) {
    return new Process(this.machineUrl, process_id, this.headers)
  }
}

class Agent {
  private readonly machineUrl: string
  private readonly agent: string
  private readonly process_id: string
  private readonly headers: Record<string, string>

  constructor(machineUrl: string, agent: string, process_id: string, headers: Record<string, string> = {}) {
    this.machineUrl = machineUrl
    this.agent = agent
    this.headers = headers
    this.process_id = process_id
  }

  public async programs() {
    const results = await fetch(`${this.machineUrl}/agents/${this.agent}/programs`, {headers: this.headers})
    if (results.status !== 200) {
      throw new HttpException(`Failed to fetch programs: ${results.statusText}`, results.status)
    }
    return await results.json() as string[]
  }

  public async action(action: string, body: Record<string, any>) {
    const results = await fetch(`${this.machineUrl}/processes/${this.process_id}/agent/${this.agent}/actions/${action}`, {
      headers: {
        "accept": "application/json",
        ...this.headers
      },
      method: 'POST',
      body: JSON.stringify(body)
    })
    if (results.status !== 200) {
      throw new HttpException(`Failed to execute action: ${results.statusText}`, results.status)
    }
    return (await results.json()) as ProcessStatusWithData
  }

  public async* stream_action(action: string, body: Record<string, any>): AsyncGenerator<ChatEvent> {
    const decoder = new TextDecoder();
    const path = `${this.machineUrl}/processes/${this.process_id}/agent/${this.agent}/actions/${action}`

    const response = await fetch(path, {
      method: "POST",
      body: JSON.stringify(body),
      headers: {
        "accept": "text/event-stream",
        ...this.headers
      }
    })
    if (response.status !== 202) {
      console.error("Failed to execute action", response.statusText, response.status)
      throw new HttpException(`Failed to execute action: ${response.statusText}`, response.status)
    }
    if (response.body) {
      const reader = response.body.getReader();
      const retStream = new ReadableStream({
        start: async (controller) => {
          try {
            const processChunk = (chunk: string) => {
              try {
                const eventSourceParser = createParser((inEvent: ParseEvent) => {
                  const event = inEvent as ParsedEvent
                  const data = JSON.parse(event.data) as ChatEvent
                  controller.enqueue(data)
                })
                eventSourceParser.feed(chunk)
              } catch (error) {
                console.error('Error parsing data:', error);
              }
            };
            // eslint-disable-next-line no-constant-condition
            while (true) {
              const {done, value} = await reader.read();
              if (done) break;
              const chunk = decoder.decode(value, {stream: true});
              processChunk(chunk);
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


      const stream = retStream.getReader()
      while (true) {
        const {done, value} = await stream.read()
        if (done) {
          break
        }
        yield value
      }
    } else {
      throw new HttpException(`Failed to obtain stream: ${response.statusText}`, response.status)
    }
  }
}

class Process {
  private readonly headers: Record<string, string>
  readonly machineUrl: string
  readonly process_id: string

  constructor(machineUrl: string, process_id: string, headers: Record<string, string> = {}) {
    this.machineUrl = machineUrl
    this.process_id = process_id
    this.headers = headers
  }

  public async status() {
    const results = await fetch(`${this.machineUrl}/processes/${this.process_id}`, {headers: this.headers})
    if (results.status !== 200) {
      throw new HttpException(`Failed to fetch process status: ${results.statusText}`, results.status)
    }
    let process = await results.json() as ProcessStatus;
    addMachineIfMissing(this.machineUrl, process)
    return process
  }

  public async delete() {
    const results = await fetch(`${this.machineUrl}/processes/${this.process_id}`, {headers: this.headers, method: 'DELETE'})
    if (results.status !== 200) {
      throw new HttpException(`Failed to delete process: ${results.statusText}`, results.status)
    }
  }

  public async upload_file(contents: Blob, mime_type: string | null = null) {
    const headers: Record<string, any> = {...this.headers, "Content-Type": "application/octet-stream", "Accept": "application/json"}
    if (mime_type) {
      headers["mime-type"] = mime_type
    }
    const results = await fetch(`${this.machineUrl}/processes/${this.process_id}/files`, {
      headers: headers,
      method: 'POST',
      body: contents
    })
    if (results.status !== 200) {
      console.error("Failed to upload file", results.statusText, results.status)
      throw new HttpException(`Failed to upload file: ${results.statusText}`, results.status)
    }
    return (await results.json()) as FileHandle
  }

  public async set_metadata(file_id: string, metadata: Record<string, any>) {
    const headers: Record<string, any> = {...this.headers, "Content-Type": "application/json", "Accept": "application/json"}
    const results = await fetch(`${this.machineUrl}/processes/${this.process_id}/files/${file_id}/metadata`, {
      headers: headers,
      method: 'POST',
      body: JSON.stringify(metadata)
    })
    if (results.status !== 200) {
      console.error("Failed to update metadata", results.statusText, results.status)
      throw new HttpException(`Failed to update metadata: ${results.statusText}`, results.status)
    }
    return (await results.json()) as FileHandle
  }

  public async download_file(file_id: string) {
    const results = await fetch(`${this.machineUrl}/processes/${this.process_id}/files/${file_id}`, {headers: this.headers})
    if (results.status !== 200) {
      throw new HttpException(`Failed to download file: ${results.statusText}`, results.status)
    }
    return {data: await results.blob(), "mimetype": results.headers.get("Content-Type")}
  }

  public async delete_file(file_id: string) {
    const results = await fetch(`${this.machineUrl}/processes/${this.process_id}/files/${file_id}`, {headers: this.headers, method: 'DELETE'})
    if (results.status !== 200) {
      throw new HttpException(`Failed to delete file: ${results.statusText}`, results.status)
    }
  }

  public async events() {
    const results = await fetch(`${this.machineUrl}/processes/${this.process_id}/events`, {headers: this.headers})
    if (results.status !== 200) {
      throw new HttpException(`Failed to fetch process events: ${results.statusText}`, results.status)
    }
    return await results.json() as ChatEvent[]
  }

  public agent(agentName: string) {
    return new Agent(this.machineUrl, agentName, this.process_id, this.headers)
  }
}
