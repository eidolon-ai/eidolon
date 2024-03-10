
// @ts-ignore
import {Avatar, Divider} from "@mui/material";
import * as React from "react";
import {AgentStartElement, DisplayElement, ErrorElement, JsonElement, MarkdownElement, ToolCallElement, UserRequestElement} from "../lib/display-elements.js";
import {ToolCall} from "./tool-call-element.js";
import {OperationInfo} from "@repo/eidolon-client/client";
import {EidolonMarkdown} from "./eidolon-markdown.js";

export interface ChatDisplayElementProps {
  rawElement: DisplayElement
  agentName: string
  topLevel: boolean
  handleAction: (operation: OperationInfo, data: Record<string, any>) => void
  userImage?: string
}

export const ChatDisplayElement = ({rawElement, agentName, topLevel, handleAction, userImage}: ChatDisplayElementProps) => {
  const getUserInput = (element: UserRequestElement) => {
    // todo, make sure this renders file inputs correctly
    let content = {...element.content}
    delete content["process_id"]
    if (Object.keys(content).length === 0) {
      return "*No Input*"
    } else if (Object.keys(content).length === 1) {
      content = content[Object.keys(content)[0]!]
    }
    content = JSON.stringify(content, undefined, "  ")
    return '```json\n' + content + "\n```"
  }

  switch (rawElement.type) {
    case "agent-start": {
      const element = rawElement as AgentStartElement
      return (
        <div>
          <div className={"chat-title"}><Avatar sx={{height: "36px", width: "36px"}} src="/eidolon_with_gradient.png"/>
            <span style={{marginLeft: '8px'}}>{element.agentName} started action {element.callName}</span></div>
        </div>
      )
    }
    case "user-request": {
      const element = rawElement as UserRequestElement
      return (
        <div>
          <div className={"chat-title"}>{topLevel ?
            <Avatar sx={{height: "32px", width: "32px"}} src={userImage!}/> :
            <Avatar sx={{height: "36px", width: "36px"}} src="/eidolon_with_gradient.png"/>}
            <span style={{marginLeft: '8px'}}>{topLevel ? "User" : "Agent Input"}</span></div>
          <div className={"chat-indent"}>
            <EidolonMarkdown>{getUserInput(element)}</EidolonMarkdown>
          </div>
        </div>
      )
    }
    case "markdown": {
      const element = rawElement as MarkdownElement
      return (
        <div className={"chat-indent"}>
          <EidolonMarkdown>{element.content}</EidolonMarkdown>
        </div>
      )
    }
    case "json": {
      const element = rawElement as JsonElement
      return (
        <div className={"chat-indent"}>
          <EidolonMarkdown>{'```json\n' + JSON.stringify(element.content, undefined,
            "  ") + "\n```"}</EidolonMarkdown>
        </div>
      )
    }
    case "tool-call": {
      const element = rawElement as ToolCallElement
      return (
        <div className={"chat-indent"}>
          <ToolCall element={element} agentName={agentName} handleAction={handleAction}/>
        </div>
      )
    }
    case "success": {
      return (
        <Divider sx={{margin: "16px 0 16px 0"}} variant={"middle"}/>
      )
    }
    case "error": {
      const element = rawElement as ErrorElement
      return (
        <div>
          <span className={"chat-title"}>Error</span>
          <div className={"chat-indent"}>
            <EidolonMarkdown>{element.reason}</EidolonMarkdown>
          </div>
        </div>
      )
    }
    case "canceled": {
      return (
        <div>
          <span className={"chat-canceled"}>Operation Canceled or Interrupted</span>
        </div>
      )
    }
  }
}
