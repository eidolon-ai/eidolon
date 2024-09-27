import {HttpException, OperationInfo} from "@eidolon-ai/client";
import {EidolonApp} from "../lib/util.ts";

export async function getAgents(machineUrl: string) {
  return fetch(`/api/eidolon/machine?machineURL=${machineUrl}`, {
    method: "GET"
  })
    .then(resp => {
      if (resp.status !== 200) {
        throw new HttpException(`Failed to fetch processes: ${resp.statusText}`, resp.status)
      }
      return resp.json().then((json) => json as string[])
    })
}

export async function getOperations(machineUrl: string, agent: string): Promise<OperationInfo[]> {
  return await fetch(`/api/eidolon/machine/${agent}?machineURL=${machineUrl}`, {
    method: "GET"
  }).then(resp => {
    if (resp.status !== 200) {
      throw new HttpException(`Failed to fetch processes: ${resp.statusText}`, resp.status)
    }
    return resp.json().then((json) => json as OperationInfo[])
  })
}

export async function getApps(): Promise<Record<string, EidolonApp>> {
  return fetch(`/api/eidolon/apps`, {
    method: "GET"
  })
    .then(async resp => {
      if (resp.status !== 200) {
        throw new HttpException(`Failed to fetch processes: ${resp.statusText}`, resp.status)
      }
      return resp.json().then((json) => json as Record<string, EidolonApp>)
    })
}

export async function getApp(appName: string): Promise<EidolonApp | undefined> {
  const apps = await getApps();
  return apps[appName]
}
