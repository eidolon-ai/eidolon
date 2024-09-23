// @ts-ignore
import {AgentStartElement, DisplayElement, ErrorElement, JsonElement, MarkdownElement, ToolCallElement, UserRequestElement} from "../lib/display-elements.ts";
import {ToolCall} from "./tool-call-element.tsx";
import {EidolonMarkdown} from "./eidolon-markdown.tsx";
import styles from "./eidolon-events.module.css"
import {AgentCall} from "./agent-element.js";
import {UserRequestUIElement} from "./user-request.js";

export interface ChatDisplayElementProps {
  machineUrl: string
  rawElement: DisplayElement
  agentName: string
  topLevel: boolean
  userImage: string | null | undefined
  userName: string | null | undefined
  depth: number
}

export const ChatDisplayElement = ({machineUrl, rawElement, agentName, topLevel, userImage, userName, depth}: ChatDisplayElementProps) => {
  if (rawElement.hidden) {
    return null
  }
  switch (rawElement.type) {
    case "agent-start": {
      const agentStart = rawElement as AgentStartElement;
      if (agentStart.children.length === 0) {
        return null
      }
      return <AgentCall machineUrl={machineUrl} element={agentStart} agentName={agentName}/>
    }
    case "user-request": {
      return <UserRequestUIElement element={rawElement as UserRequestElement} topLevel={topLevel} userName={userName} userImage={userImage} machineUrl={machineUrl}/>
    }
    case "markdown": {
      const element = rawElement as MarkdownElement
      return (
        <div className={styles[`chat-indent`]}>
          <EidolonMarkdown machineUrl={machineUrl}>{element.content}</EidolonMarkdown>
        </div>
      )
    }
    case "json": {
      const element = rawElement as JsonElement
      return (
        <div className={styles[`chat-indent`]}>
          <EidolonMarkdown machineUrl={machineUrl}>{'```json\n' + JSON.stringify(element.content, undefined,
            "  ") + "\n```"}</EidolonMarkdown>
        </div>
      )
    }
    case "tool-call": {
      const element = rawElement as ToolCallElement
      return (
        <div className={styles[`chat-indent`]}>
          <ToolCall machineUrl={machineUrl} element={element} agentName={agentName} depth={depth}/>
        </div>
      )
    }
    case "error": {
      const element = rawElement as ErrorElement
      return (
        <div>
          <span className={styles[`chat-title`]}>Error</span>
          <div className={styles[`chat-indent`]}>
            <EidolonMarkdown machineUrl={machineUrl}>{element.reason}</EidolonMarkdown>
          </div>
        </div>
      )
    }
    case "canceled": {
      return (
        <div>
          <span className={styles[`chat-canceled`]}>Operation Canceled or Interrupted</span>
        </div>
      )
    }
  }
}
