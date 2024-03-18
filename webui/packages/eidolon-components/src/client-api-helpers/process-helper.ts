import {DateTime} from "luxon";
import {ProcessStatus} from "@eidolon/client";

export interface ProcessStatusWithChildren extends ProcessStatus {
  children?: ProcessStatus[]
}

export async function getProcessStatus(process_id: string) {
    return fetch(`/api/eidolon/process/${process_id}`)
        .then(resp => {
            if (resp.status === 404) {
                return null
            }
            return resp.json().then((json: Record<string, any>) => json as ProcessStatus)
        })
}

export async function deleteProcess(process_id: string) {
  await fetch(`/api/eidolon/process/${process_id}`, {
    method: "DELETE",
  })
}

export async function getRootProcesses(): Promise<ProcessStatusWithChildren[]> {
  let data = (await getProcessesFromServer()).sort((a, b) => {
    return DateTime.fromISO(b.updated).toMillis() - DateTime.fromISO(a.updated).toMillis()
  })
  return Object.values(data.reduce((collector: Record<string, ProcessStatusWithChildren>, item) => {
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
  }, {} as Record<string, ProcessStatus>))

}

async function getProcessesFromServer(): Promise<ProcessStatus[]> {
  const results = await fetch(`/api/eidolon/process`,
    {
      // @ts-ignore
      next: {tags: ['chats']},
    }
  ).then(resp => {
    if (resp.status === 401) {
      console.log('Unauthenticated! Status: 401');
      return [];
    } else if (!resp.ok) {
      throw new Error(`HTTP error! status: ${resp.status}`);
    }
    return resp.json();
  })

  const ret = []
  for (const json of results.processes) {
    json.id = json.process_id
    json.title = json.title || json.agent
    json.path = `/chat/${json.id}`
    ret.push(json as ProcessStatus)
  }

  return ret
}
