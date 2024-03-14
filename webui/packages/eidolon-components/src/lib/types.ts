import OpenAPIParser from "@readme/openapi-parser";
import {OpenAPIV3_1} from "openapi-types";

export interface ProcessStatus extends Record<string, any> {
  process_id: string
  parent_process_id?: string
  title: string
  agent: string
  state: string
  created: string
  updated: string
  children?: ProcessStatus[]
}
