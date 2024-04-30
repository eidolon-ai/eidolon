// @ts-ignore
import {Avatar, Divider} from "@mui/material";
import {AgentStartElement, DisplayElement, ErrorElement, JsonElement, MarkdownElement, ToolCallElement, UserRequestElement} from "../lib/display-elements";
import {ToolCall} from "./tool-call-element";
import {EidolonMarkdown} from "./eidolon-markdown";

export interface ChatDisplayElementProps {
  machineUrl: string
  rawElement: DisplayElement
  agentName: string
  topLevel: boolean
  userImage?: string
}

export const ChatDisplayElement = ({machineUrl, rawElement, agentName, topLevel, userImage}: ChatDisplayElementProps) => {
  const getUserInput = (element: UserRequestElement) => {
    let content = typeof element.content === "string" ? {body: element.content} : {...element.content}
    delete content["process_id"]
    if (Object.keys(content).length === 0) {
      return "*No Input*"
    } else if (Object.keys(content).length === 1 && Object.keys(content)[0] === "body") {
      return content[Object.keys(content)[0]!]
    } else {
      content = JSON.stringify(content, undefined, "  ")
      return '```json\n' + content + "\n```"
    }
  }

  switch (rawElement.type) {
    case "agent-start": {
      const element = rawElement as AgentStartElement
      return (
        <div>
          <div className={"chat-title"}><Avatar sx={{height: "36px", width: "36px"}} src="/img/eidolon_with_gradient.png"/>
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
            <Avatar sx={{height: "36px", width: "36px"}} src="/img/eidolon_with_gradient.png"/>}
            <span style={{marginLeft: '8px'}}>{topLevel ? "User" : "Agent Input"}</span></div>
          <div className={"chat-indent"}>
            <EidolonMarkdown machineUrl={machineUrl}>{getUserInput(element)}</EidolonMarkdown>
          </div>
        </div>
      )
    }
    case "markdown": {
      const element = rawElement as MarkdownElement
      return (
        <div className={"chat-indent"}>
          <EidolonMarkdown machineUrl={machineUrl}>{element.content}</EidolonMarkdown>
        </div>
      )
    }
    case "json": {
      const element = rawElement as JsonElement
      return (
        <div className={"chat-indent"}>
          <EidolonMarkdown machineUrl={machineUrl}>{'```json\n' + JSON.stringify(element.content, undefined,
            "  ") + "\n```"}</EidolonMarkdown>
        </div>
      )
    }
    case "tool-call": {
      const element = rawElement as ToolCallElement
      return (
        <div className={"chat-indent"}>
          <ToolCall machineUrl={machineUrl} element={element} agentName={agentName}/>
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
            <EidolonMarkdown machineUrl={machineUrl}>{element.reason}</EidolonMarkdown>
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
