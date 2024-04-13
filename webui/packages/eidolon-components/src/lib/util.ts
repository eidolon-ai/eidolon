import {OperationInfo} from "@eidolon/client";

export interface CopilotParams {
  "agent": string,
  supportedLLMs: string[] | undefined,
  defaultLLM: string | undefined,
  operation: OperationInfo,
  "inputLabel": string,
  "titleOperationName": string | undefined,
  "allowSpeech": boolean,
  "speechAgent": string | undefined,
  "speechOperation": string | undefined
}
export interface DevParams {
}
