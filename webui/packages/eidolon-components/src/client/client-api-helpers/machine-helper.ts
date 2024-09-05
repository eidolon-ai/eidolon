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
      return resp.json().then((json: Record<string, any>) => json as string[])
    })
}

export async function getOperations(machineUrl: string, agent: string) {
  return await fetch(`/api/eidolon/machine/${agent}?machineURL=${machineUrl}`, {
    method: "GET"
  }).then(resp => {
      if (resp.status !== 200) {
        throw new HttpException(`Failed to fetch processes: ${resp.statusText}`, resp.status)
      }
    return resp.json().then((json: Record<string, any>) => json as OperationInfo[])
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
      return resp.json().then((json: Record<string, any>) => json as Record<string, EidolonApp>)
    })
}
