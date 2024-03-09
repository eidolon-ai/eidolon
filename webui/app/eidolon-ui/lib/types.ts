import OpenAPIParser from "@readme/openapi-parser";
import {OpenAPIV3_1} from "openapi-types";
import {getAuthHeaders} from "@/app/api/chat/messages/chatHelpers";

export interface Chat extends Record<string, any> {
  id: string
  title: string
  agent: string
  state: string
  process_id: string
  parent_process_id?: string
  created: string
  updated: string
  userId: string
  path: string
  sharePath?: string
  children?: Chat[]
}

export interface OperationInfo {
  label: string
  agent: string
  name: string
  path: string
  summary?: string
  description?: string
  schema: OpenAPIV3_1.SchemaObject
}

export interface ChatEvent extends Record<string, any> {
  event_type: string,
  category: string,
}

export class EidolonClient {
  private machineUrl: string
  private isLoaded = false

  private actions: Record<string, OperationInfo> = {}
  private agents: string[] = []

  constructor(machineUrl: string) {
    this.machineUrl = machineUrl
  }

  private processRequestBody(agent: string, name: string, path: string, requestBody: any) {
    const ret = {
      label: `${agent}:${name}`,
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
      const auth_headers = await getAuthHeaders()
      const results = await fetch(`${this.machineUrl}/openapi.json`,{headers: auth_headers})
      if (results.status !== 200) {
        throw new Error(`Failed to fetch openapi.json: ${results.statusText}`)
      }
      const response = await results.json()
      const api = await OpenAPIParser.validate(response) as OpenAPIV3_1.Document
      const paths = api.paths!
      const agentRE = /\/agents\/([^/]+)/
      const agents = new Set<string>()
      for (const path in paths) {
        if (paths[path]?.post) {
          const requestBody = paths[path]!.post!.requestBody
          const agentName = agentRE.exec(path)![1]
          agents.add(agentName)
          let opName = path.substring(path.lastIndexOf('/') + 1);
          if (path.includes("process")) {
            this.actions[agentName + "-" + opName] = this.processRequestBody(agentName, opName, path, requestBody)
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

  public async getActionsForDisplay(agent: string, availableActions: string[]) {
    const ret = Object.values(await this.getActions())
      .filter(op => op.agent === agent && availableActions.includes(op.name))
      .sort((a, b) => a.label.localeCompare(b.label))
    for (const op of ret) {
      this.convertBinary(op.schema)
    }
    return ret
  }
}

export interface ProcessState {
  state: string,
  available_actions: string[]
  error?: string
}

