import appRegistry from 'eidolon-apps.json'


export interface EidolonApp {
  name: string;
  description: string;
  version: string;
  image: string;
  location: string;
  type: "copilot" | "dev"
  path: string
  params: CopilotParams | DevParams
}

export interface DevParams {
}

export interface CopilotParams {
  "agent": string,
  "operation": string,
  "inputLabel": string,
  "titleOperationName": string | undefined,
  "allowSpeech": boolean,
  "speechAgent": string | undefined,
  "speechOperation": string | undefined
}

interface RawAgentLocation {
  agent: string | undefined
  machine: string
}

export interface AgentLocation {
  agent: string
  machine: string
}

const agentRegistry: Record<string, AgentLocation> = {}
if (process.env.EIDOLON_AGENT_REGISTRY) {
  const registry: Record<string, RawAgentLocation> = JSON.parse(process.env.EIDOLON_AGENT_REGISTRY)
  for (const [key, value] of Object.entries(registry)) {
    if (!value.agent) {
      value.agent = key
    }
    agentRegistry[key] = value as AgentLocation
  }
}

let apps: Record<string, EidolonApp> = {}

for (const [key, value] of Object.entries(appRegistry)) {
  const app = value as EidolonApp
  const image = await import(`../../app/eidolon-apps/${key}/${app.image}`)
  app.path = `${key}`
  if (app.type === 'copilot') {
    app.path = `sp/${key}`
    const params = app.params as CopilotParams
    if (params.agent in agentRegistry) {
      const location = agentRegistry[params.agent]!
      params.agent = location.agent
      app.location = location.machine
    }
  }
  app.image = image.default.src
  apps[key] = app
}

export function getAppRegistry() {
  return apps
}

export function getApp(path: string) {
  return apps[path]
}
