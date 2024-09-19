import {HttpException, OperationInfo} from "@eidolon-ai/client";

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

export interface CopilotParams {
  type: "copilot",
  "agent": string,
  custom_page: string | undefined,
  addBtnText: string | undefined,
  newItemText: string | undefined,
  supportedLLMs: string[] | undefined,
  defaultLLM: string | undefined,
  operation: string,
  operationInfo: OperationInfo,
  "inputLabel": string,
  "titleOperationName": string | undefined,
  "allowSpeech": boolean,
  "speechAgent": string | undefined,
  "speechOperation": string | undefined
}

export interface DevParams {
  type: "dev",
  agent: string,
  operations: OperationInfo[],
  addBtnText: string | undefined,
  newItemText: string | undefined,
}


export function processResponse(promise: Promise<any>) {
  return convertException(promise.then(Response.json))
}

export function convertException(promise: Promise<any>) {
  return promise.catch((e) => {
    if (e instanceof HttpException) {
      return new Response(e.statusText, {status: e.status, statusText: e.statusText})
    } else if (e instanceof Error) {
      // @ts-ignore
      if (e?.cause?.code === 'ECONNREFUSED') {
        return new Response('Server Down', {status: 503})
      }

      return new Response(e.message, {status: 500})
    } else {
      if (e?.cause?.code === 'ECONNREFUSED') {
        return new Response('Server Down', {status: 503})
      }

      return new Response('Unknown error', {status: 500})
    }
  })
}
