import {HttpException, OperationInfo} from "@eidolon/client";

export interface CopilotParams {
  "agent": string,
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
}


export function processResponse(promise: Promise<any>) {
  return convertException(promise.then(Response.json))
}

export function convertException(promise: Promise<any>) {
  return promise.catch((e) => {
    if (e instanceof HttpException) {
      return new Response(e.statusText, {status: e.status, statusText: e.statusText})
    } else if (e instanceof Error) {
      return new Response(e.message, {status: 500})
    } else {
      if (e?.cause?.code === 'ECONNREFUSED') {
        return new Response('Connection refused', {status: 404})
      }

      return new Response('Unknown error', {status: 500})
    }
  })
}
