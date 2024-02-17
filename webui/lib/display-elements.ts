import {ChatEvent} from "@/lib/types";

export interface DisplayElement {
  type: string
}

export interface AgentStartElement extends DisplayElement {
  type: "agent-start",
  agentName: string
  callName: string
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
  content: any
}

export interface MarkdownElement extends DisplayElement {
  type: "markdown",
  content: string
}

export interface JsonElement extends DisplayElement {
  type: "json",
  content: any
}

export interface ToolCallElement extends DisplayElement {
  type: "tool-call",
  title: string,
  sub_title: string,
  is_active: boolean,
  is_agent: boolean,
  contextId: string,
  children: DisplayElement[]
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
}

export const makeElement = (event: ChatEvent) => {
  switch (event.event_type) {
    case "agent_call":
      return {
        type: "agent-start",
        agentName: event.agent_name,
        callName: event.call_name
      } as AgentStartElement
    case "success":
      return {
        type: "success"
      } as SuccessElement
    case "error":
      return {
        type: "error",
        reason: event.reason
      } as ErrorElement
    case "canceled":
      return {
        type: "canceled"
      } as CanceledElement
    case "user_input":
      return {
        type: "user-request",
        content: event.input
      } as UserRequestElement
    case "string":
      return {
        type: "markdown",
        content: event.content
      } as MarkdownElement
    case "object":
      return {
        type: "json",
        content: event.content
      } as JsonElement
    case "tool_call_start":
      return {
        type: "tool-call",
        title: event.title || event.tool_call.name,
        sub_title: event.sub_title || "",
        is_active: true,
        is_agent: event.is_agent_call || false,
        contextId: event.context_id,
        children: []
      } as ToolCallElement
    case "context_end":
      return {
        type: "tool-call-end",
        contextId: event.context_id
      } as ToolCallEndElement
    case "agent_state":
      return {
        type: "agent-state",
        state: event.state,
        availableActions: event.available_actions
      } as AgentStateElement
  }

  return undefined
}
