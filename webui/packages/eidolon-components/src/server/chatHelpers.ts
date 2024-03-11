// noinspection JSUnusedGlobalSymbols

'use server'

import {Chat} from "../lib/types.js";
import {ChatEvent, ProcessState} from "@repo/eidolon-client/client";

const chatServerURL = process.env.EIDOLON_SERVER

export const getAuthHeaders = async (access_token: string | undefined): Promise<Record<string, string>> => {
  if (!access_token) {
    return {} as Record<string, string>
  }
  return {
    "Authorization": `Bearer ${access_token}`
  }
}

export async function getChatEvents(access_token: string | undefined, agentName: string, processId: string) {
  const auth_headers = await getAuthHeaders(access_token)
  const results = await fetch(`${chatServerURL}/agents/${agentName}/processes/${processId}/events`, {headers: auth_headers})
    .then(resp => resp.json())

  const ret = []
  for (const json of results) {
    ret.push(json as ChatEvent)
  }

  return ret
}


export async function getChat(access_token: string | undefined, id: string) {
  const auth_headers = await getAuthHeaders(access_token)
  if (!auth_headers || !id) {
    return null
  }
  const json = await fetch(`${chatServerURL}/system/processes/${id}`, {headers: auth_headers}).then(resp => {
    if (resp.ok) {
      return resp.json()
    } else {
      console.log("error", resp)
      return undefined
    }
  })

  if (json) {
    json.id = json.process_id
    json.title = json.title || json.agent
    json.path = `/chat/${json.id}`
  }
  return json as Chat
}

export async function deleteChat(access_token: string | undefined, agentName: string, process_id: string) {
  const auth_headers = await getAuthHeaders(access_token)
  await fetch(`${chatServerURL}/agents/${agentName}/processes/${process_id}`, {
    method: "DELETE",
    headers: auth_headers
  })
}

export async function getChats(access_token: string | undefined): Promise<Chat[]> {
  const auth_headers = await getAuthHeaders(access_token)
  const results = await fetch(`${chatServerURL}/system/processes`,
    {
      // @ts-ignore
      next: {tags: ['chats']},
      headers: auth_headers
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
  for (const json of results) {
    json.id = json.process_id
    json.title = json.title || json.agent
    json.path = `/chat/${json.id}`
    ret.push(json as Chat)
  }

  return ret
}

/**
 * Create a new process. Make sure you invalidate the tag `chats` after calling this function
 * @param access_token
 * @param agentName
 * @param title
 */
export async function createPID(access_token: string | undefined, agentName: string, title: string) {
  const auth_headers = await getAuthHeaders(access_token)
  const body = {title: title}
  const results = await fetch(`${chatServerURL}/agents/${agentName}/processes`, {
    method: "POST",
    body: JSON.stringify(body),
    headers: {
      "Content-Type": "application/json",
      ...auth_headers
    }
  })

  const json = await results.json()
  return json["process_id"]
}

export async function getPIDStatus(access_token: string | undefined, agentName: string, process_id: string) {
  const auth_headers = await getAuthHeaders(access_token)
  return fetch(`${chatServerURL}/agents/${agentName}/processes/${process_id}/status`, {headers: auth_headers})
    .then(resp => {
      if (resp.status === 404) {
        return null
      }
      return resp.json().then((json: Record<string, any>) => json as ProcessState)
    })
}
