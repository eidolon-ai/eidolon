import appRegistry from 'eidolon-apps.json'


export interface EidolonApp {
  name: string;
  description: string;
  version: string;
  image: string;
}

let apps: Record<string, EidolonApp> = {}

for (const [key, value] of Object.entries(appRegistry)) {
  apps[key] = value as EidolonApp
  const image = await import(`../../app/eidolon-apps/${key}/${apps[key]!.image}`)
  apps[key]!.image = image.default.src
}

export function getAppRegistry() {
  return apps
}
