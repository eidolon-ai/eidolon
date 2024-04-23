import _appRegistry from 'eidolon-apps.json'
import {CopilotParams, EidolonApp} from "@eidolon/components";
import * as fs from "fs";
import {notFound} from "next/navigation";

let appRegistry = _appRegistry
if (process.env.EIDOLON_APP_REGISTRY_OVERRIDE) {
  appRegistry = JSON.parse(process.env.EIDOLON_APP_REGISTRY_OVERRIDE)
} else if (process.env.EIDOLON_APP_REGISTRY_LOC) {
  const rawData = fs.readFileSync(process.env.EIDOLON_APP_REGISTRY_LOC, {encoding: 'utf8'});
  appRegistry = JSON.parse(rawData)
}


interface RawAgentLocation {
  agent: string | undefined
  machine: string
}

export interface AgentLocation {
  agent: string
  machine: string
}

// our cached functions cannot be async, so we cannot use. We have the same issue when dynamically loading appRegistry
for (const [key, value] of Object.entries(appRegistry)) {
  const app = value as EidolonApp
  const image = await import(`../../app/eidolon-apps/${key}/${app.image}`)
  app.image = image.default.src
}


function getAgentRegistry() {
  const agentRegistry: Record<string, AgentLocation> = {}
  if (process.env.EIDOLON_AGENT_REGISTRY) {
    try {
      const registry: Record<string, RawAgentLocation> = JSON.parse(process.env.EIDOLON_AGENT_REGISTRY)
      for (const [key, value] of Object.entries(registry)) {
        if (!value.agent) {
          value.agent = key
        }
        agentRegistry[key] = value as AgentLocation
      }
    } catch (e) {
      console.error("Failed to parse agent registry with error ", e)
    }
  }
  if (process.env.EIDOLON_AGENT_REGISTRY_LOC) {
    try {
      const rawData = fs.readFileSync(process.env.EIDOLON_AGENT_REGISTRY_LOC, {encoding: 'utf8'});
      const registry: Record<string, RawAgentLocation> = JSON.parse(rawData)
      for (const [key, value] of Object.entries(registry)) {
        if (!value.agent) {
          value.agent = key
        }
        agentRegistry[key] = value as AgentLocation
      }
    } catch (e) {
      console.error("Failed to parse agent registry from file with error ", e)
    }
  }
  return agentRegistry
}


function getAppsRaw() {
  console.log("Building Apps")
  if (process.env.EIDOLON_SERVER) {
    console.log("Overriding app location:", process.env.EIDOLON_SERVER)
  }
  let apps: Record<string, EidolonApp> = {}
  const agentRegistry = getAgentRegistry()
  for (const [key, value] of Object.entries(appRegistry)) {
    const app = value as EidolonApp
    app.path = `${key}`
    if (app.type === 'copilot') {
      app.path = `sp/${key}`
      const params = app.params as CopilotParams
      if (params.agent in agentRegistry) {
        const location = agentRegistry[params.agent]!
        params.agent = location.agent
        app.location = location.machine
        console.log("setting ", params.agent, " machine ", location.machine)
      }
    }
    if (process.env.EIDOLON_SERVER) {
      app.location = process.env.EIDOLON_SERVER
    }
    apps[key] = app
  }
  return apps
}

let apps: Record<string, EidolonApp> | undefined = undefined

export function getAppRegistry() {
  if (apps === undefined) {
    apps = getAppsRaw()
  }
  return apps
}


export function getApp(path: string): EidolonApp {
  let app = getAppRegistry()[path];
  if (!app) {
    notFound()
  } else {
    return app
  }
}
