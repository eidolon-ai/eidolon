// @ts-ignore
import {AgentStartElement, DisplayElement, ErrorElement, JsonElement, MarkdownElement, ToolCallElement, UserRequestElement} from "../lib/display-elements.ts";
import {ToolCall} from "./tool-call-element.tsx";
import {EidolonMarkdown} from "./eidolon-markdown.tsx";
import styles from "./eidolon-events.module.css"
import {AgentCall} from "./agent-element.js";
import {UserRequestUIElement} from "./user-request.js";

export interface ChatDisplayElementProps {
  rawElement: DisplayElement
  agentName: string
  topLevel: boolean
  userImage: string | null | undefined
  userName: string | null | undefined
  depth: number
  goToProcess: (processId: string) => void;
}

export const ChatDisplayElement = ({rawElement, agentName, topLevel, userImage, userName, depth, goToProcess}: ChatDisplayElementProps) => {
  if (rawElement.metadata?.eidolon?.internal) {
    return null
  }

  switch (rawElement.type) {
    case "agent-start": {
      const agentStart = rawElement as AgentStartElement;
      if (agentStart.children.length === 0) {
        return null
      }
      return <AgentCall element={agentStart} agentName={agentName} goToProcess={goToProcess}/>
    }
    case "user-request": {
      return <UserRequestUIElement element={rawElement as UserRequestElement} topLevel={topLevel} userName={userName} userImage={userImage}/>
    }
    case "markdown": {
      const element = rawElement as MarkdownElement
      return (
        <div className={styles[`chat-indent`]}>
          <EidolonMarkdown>{element.content}</EidolonMarkdown>
        </div>
      )
    }
    case "json": {
      const element = rawElement as JsonElement
      return (
        <div className={styles[`chat-indent`]}>
          <EidolonMarkdown>{'```json\n' + JSON.stringify(element.content, undefined,
            "  ") + "\n```"}</EidolonMarkdown>
        </div>
      )
    }
    case "tool-call": {
      const element = rawElement as ToolCallElement
      return (
        <div className={styles[`chat-indent`]}>
          <ToolCall element={element} agentName={agentName} depth={depth} goToProcess={goToProcess}/>
        </div>
      )
    }
    case "error": {
      const element = rawElement as ErrorElement
      return (
        <div>
          <span className={styles[`chat-title`]}>Error</span>
          <div className={styles[`chat-indent`]}>
            <EidolonMarkdown>{element.reason}</EidolonMarkdown>
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
