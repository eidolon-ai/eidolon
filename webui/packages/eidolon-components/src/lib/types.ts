import OpenAPIParser from "@readme/openapi-parser";
import {OpenAPIV3_1} from "openapi-types";

export interface Chat extends Record<string, any> {
  id: string
  title: string
  agent: string
  state: string
  process_id: string
  parent_process_id?: string
  created: string
  updated: string
  path: string
  sharePath?: string
  children?: Chat[]
}
