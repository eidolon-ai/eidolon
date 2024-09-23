// @ts-ignore
import {AgentStartElement, DisplayElement, ErrorElement, JsonElement, MarkdownElement, ToolCallElement, UserRequestElement} from "../lib/display-elements.ts";
import {ToolCall} from "./tool-call-element.tsx";
import {EidolonMarkdown} from "./eidolon-markdown.tsx";
import styles from "./eidolon-events.module.css"
import {AgentCall} from "./agent-element.js";
import {useProcesses} from "../hooks/processes_context.js";

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
  const getUserInput = (element: UserRequestElement) => {
    let content: Record<string, unknown> = typeof element.content === "string" ? {body: element.content} : {...element.content as object}
    delete content["process_id"]
    if (Object.keys(content).length === 0) {
      return "*No Input*"
    } else if (Object.keys(content).length === 1 && Object.keys(content)[0] === "body") {
      return content[Object.keys(content)[0]!]
    } else {
      const contentStr = JSON.stringify(content, undefined, "  ")
      return '```json\n' + contentStr + "\n```"
    }
  }

  switch (rawElement.type) {
    case "agent-start": {
      return <AgentCall machineUrl={machineUrl} element={rawElement as AgentStartElement} agentName={agentName}/>
    }
    case "user-request": {
      const element = rawElement as UserRequestElement
      let userAvatar: JSX.Element
      let agentName = "Agent Input"
      if (topLevel) {
        if (userName) {
          agentName = userName
        } else {
          agentName = "User"
        }
      }
      if (topLevel) {
        if (userImage) {
          userAvatar = userAvatar = (
            <div className="h-6 w-6 rounded-full overflow-hidden">
              <img src={userImage!} alt="User avatar" className="w-full h-full object-cover"/>
            </div>
          )
        } else {
          userAvatar = (
            <div className="h-6 w-6 rounded-full bg-blue-500 flex items-center justify-center text-white text-xs font-medium">
              {userName?.charAt(0).toUpperCase()}
            </div>
          )
        }
      } else {
        userAvatar = (
          <div className="h-6 w-6 rounded-full overflow-hidden">
            <img src={"/img/eidolon_with_gradient.png"} alt="User avatar" className="w-full h-full object-cover"/>
          </div>
        )
      }
      return (
        <div className={"flex flex-row border-r-4 rounded-xl py-3 px-2 w-fit user-element"}
        >
          {userAvatar}
          <div className={"mx-2"}>
            <EidolonMarkdown machineUrl={machineUrl}>{getUserInput(element)}</EidolonMarkdown>
          </div>
        </div>
      )
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
