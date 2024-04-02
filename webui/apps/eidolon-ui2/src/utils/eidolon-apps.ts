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

let apps: Record<string, EidolonApp> = {}

for (const [key, value] of Object.entries(appRegistry)) {
  const app = value as EidolonApp
  const image = await import(`../../app/eidolon-apps/${key}/${app.image}`)
  app.path = `${key}`
  if (app.type === 'copilot') {
    app.path = `sp/${key}`
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
