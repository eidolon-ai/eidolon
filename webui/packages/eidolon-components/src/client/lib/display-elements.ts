import {ChatEvent} from "@eidolon-ai/client";

interface MetadataObject {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  [key: string]: any;
}

export interface DisplayElement {
  type: string;
  metadata?: MetadataObject;
}

export interface AgentStartElement extends DisplayElement {
  type: "agent-start",
  agentName: string
  callName: string
  title: string
  sub_title: string
  process_id: string
  children: DisplayElement[]
}

export interface SuccessElement extends DisplayElement {
  type: "success",
}

export interface ErrorElement extends DisplayElement {
  type: "error",
  reason: string
}

export interface CanceledElement extends DisplayElement {
  type: "canceled",
}

export interface UserRequestElement extends DisplayElement {
  type: "user-request",
  content: unknown
}

export interface MarkdownElement extends DisplayElement {
  type: "markdown",
  content: string
}

export interface JsonElement extends DisplayElement {
  type: "json",
  content: unknown
}

export interface ToolCallElement extends DisplayElement {
  type: "tool-call",
  title: string,
  sub_title: string,
  is_active: boolean,
  is_agent: boolean,
  process_id: string,
  contextId: string,
  children: DisplayElement[]
  arguments: Record<string, unknown>
}

export interface ToolCallEndElement extends DisplayElement {
  type: "tool-call-end",
  contextId: string,
}

export interface AgentStateElement extends DisplayElement {
  type: "agent-state",
  state: string
  availableActions: string[]
}

export interface ElementsAndLookup {
  elements: DisplayElement[],
  lookup: Record<string, ToolCallElement>
  rootAgent?: AgentStartElement
}

export const makeElement = (event: ChatEvent) => {
  switch (event.event_type) {
    case "agent_call":
      return {
        type: "agent-start",
        agentName: event.agent_name,
        callName: event.call_name,
        title: event.title,
        process_id: event.process_id,
        sub_title: event.sub_title,
        children: [],
        metadata: event.metadata
      } as AgentStartElement
    case "success":
      return {
        type: "success",
        metadata: event.metadata
      } as SuccessElement
    case "error":
      return {
        type: "error",
        reason: event.reason,
        metadata: event.metadata
      } as ErrorElement
    case "canceled":
      return {
        type: "canceled",
        metadata: event.metadata
      } as CanceledElement
    case "user_input":
      return {
        type: "user-request",
        content: event.input,
        metadata: event.metadata
      } as UserRequestElement
    case "string":
      return {
        type: "markdown",
        content: event.content,
        metadata: event.metadata
      } as MarkdownElement
    case "object":
      return {
        type: "json",
        content: event.content,
        metadata: event.metadata
      } as JsonElement
    case "tool_call_start":
      return {
        type: "tool-call",
        title: event.title || event.tool_call.name,
        sub_title: event.is_agent_call ? "" : (event.sub_title || ""),
        is_active: true,
        is_agent: event.is_agent_call || false,
        process_id: event.process_id,
        contextId: event.context_id,
        arguments: event.tool_call.arguments,
        children: [],
        metadata: event.metadata
      } as ToolCallElement
    case "context_start":
      return {
        type: "tool-call",
        title: event.title,
        sub_title: event.sub_title || "",
        is_active: true,
        is_agent: event.is_agent_call || false,
        contextId: event.context_id,
        process_id: event.process_id,
        children: [],
        arguments: {},
        metadata: event.metadata
      } as ToolCallElement
    case "context_end":
      return {
        type: "tool-call-end",
        contextId: event.context_id,
        metadata: event.metadata
      } as ToolCallEndElement
    case "agent_state": {
      return {
        type: "agent-state",
        state: event.state,
        availableActions: event.available_actions,
        metadata: event.metadata
      } as AgentStateElement
    }
  }

  return undefined
}
