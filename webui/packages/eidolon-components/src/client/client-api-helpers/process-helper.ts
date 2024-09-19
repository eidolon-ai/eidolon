import {DateTime} from "luxon";
import {HttpException, ProcessStatus} from "@eidolon-ai/client";

export interface ProcessStatusWithChildren extends ProcessStatus {
  children?: ProcessStatus[]
}

export async function getProcessStatus(machineUrl: string, process_id: string) {
  return fetch(`/api/eidolon/process/${process_id}?machineURL=${machineUrl}`, {
    method: "GET"
  })
    .then(resp => {
      if (resp.status !== 200) {
        throw new HttpException(`Failed to fetch processes: ${resp.statusText}`, resp.status)
      }
      return resp.json().then((json) => json as ProcessStatus)
    })
}

export async function createProcess(machineUrl: string, agent: string, title: string) {
  return await fetch(`/api/eidolon/process?machineURL=${machineUrl}`, {
    method: "POST",
    body: JSON.stringify({machineUrl, agent, title}),
  }).then(resp => {
    if (resp.status === 404) {
      return null
    }
    return resp.json().then((json) => json as ProcessStatus)
  })
}

export async function deleteProcess(machineUrl: string, process_id: string) {
  await fetch(`/api/eidolon/process/${process_id}?machineURL=${machineUrl}`, {
    method: "DELETE",
  })
}

export async function getRootProcesses(machineUrl: string): Promise<ProcessStatusWithChildren[]> {
  return getProcessesFromServer(machineUrl).then(processes => processes.sort((a, b) => {
    return DateTime.fromISO(b.updated).toMillis() - DateTime.fromISO(a.updated).toMillis()
  })).then(data => Object.values(data.reduce((collector: Record<string, ProcessStatusWithChildren>, item) => {
    if (!item.parent_process_id) {
      collector[item.process_id] = {...collector[item.process_id], ...item}
    } else {
      if (!collector[item.parent_process_id]) {
        collector[item.parent_process_id] = {
          machine: item.machine,
          agent: item.agent,
          title: item.parent_process_id,
          state: "Draft",
          available_actions: item.available_actions,
          created: item.created,
          updated: item.updated,
          process_id: item.parent_process_id,
          children: []
        }
      }
      if (!collector[item.parent_process_id]!.children) {
        collector[item.parent_process_id]!.children = []
      }
      collector[item.parent_process_id]!.children!.push(item)
    }
    return collector
  }, {} as Record<string, ProcessStatus>)))

}

export async function getProcessesFromServer(machineUrl: string): Promise<ProcessStatus[]> {
  return fetch(`/api/eidolon/process?machineURL=${machineUrl}`
  ).then(resp => {
    if (resp.status !== 200) {
      throw new HttpException(`Failed to fetch processes: ${resp.statusText}`, resp.status)
    }
    if (!resp.ok) {
      throw new Error(`HTTP error! status: ${resp.status}, status test: ${resp.statusText}`);
    }
    return resp.json();
  }).then(results => {
    const ret = []
    for (const json of results.processes) {
      json.id = json.process_id
      json.title = json.title || json.agent
      json.path = `/chat/${json.id}`
      ret.push(json as ProcessStatus)
    }

    return ret
  })

}

export function getAppPathFromPath(pathname: string): string | undefined {
  const pathSegments = pathname.split('/');
  const appNameIndex = pathSegments.findIndex((segment) => segment === 'eidolon-apps');

  if (appNameIndex !== -1 && appNameIndex + 1 < pathSegments.length) {
    return pathSegments.slice(0, appNameIndex + 2).join('/')
  }
  return undefined
}