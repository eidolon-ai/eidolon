// @ts-ignore
import {Avatar, Box, Divider, Typography} from "@mui/material";
import {AgentStartElement, DisplayElement, ErrorElement, JsonElement, MarkdownElement, ToolCallElement, UserRequestElement} from "../lib/display-elements";
import {ToolCall} from "./tool-call-element";
import {EidolonMarkdown} from "./eidolon-markdown";

export interface ChatDisplayElementProps {
  machineUrl: string
  rawElement: DisplayElement
  agentName: string
  topLevel: boolean
  userImage: string | null | undefined
  userName: string | null | undefined
}

export const ChatDisplayElement = ({machineUrl, rawElement, agentName, topLevel, userImage, userName}: ChatDisplayElementProps) => {
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
      console.log(element.agentName, element.callName, element.title, element.sub_title)
      let title: string
      let subTitle: string
      if (element.title) {
        title = element.title
        subTitle = element.callName
      } else {
        title = element.agentName
        subTitle = element.callName
      }
      return (
        <div style={{display: 'flex', flexDirection: 'column'}}>
          <div style={{display: 'flex', padding: "8px", marginBottom: "16px", background: "#f8f8f8", borderRadius: "8px", marginTop: "8px"}}>
            <Avatar sx={{height: "36px", width: "36px"}} src="/img/eidolon_with_gradient.png"/>
            <Box>
              <Typography variant={"h6"} style={{marginLeft: '8px'}}>{title}</Typography>
              <Typography lineHeight={1} variant={"subtitle1"} style={{marginLeft: '24px', color: '#777'}}>{subTitle}</Typography>
            </Box>
          </div>
        </div>
      )
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
          userAvatar = <Avatar sx={{height: "32px", width: "32px"}} src={userImage!}/>
        } else {
          userAvatar = <Avatar sx={{height: "32px", width: "32px"}}>{userName?.charAt(0)}</Avatar>
        }
      } else {
        userAvatar = <Avatar sx={{height: "24px", width: "24px"}} src="/img/eidolon_with_gradient.png"/>
      }
      return (
        <div>
          <div style={{display: 'flex', flexDirection: 'column'}}>
            <div style={{display: 'flex', padding: "8px", marginBottom: "16px", background: "#f8f8f8", borderRadius: "8px", marginTop: "8px"}}>
              {userAvatar}
              <Box>
                <Typography variant={"h6"} style={{marginLeft: '8px'}}>{agentName}</Typography>
              </Box>
            </div>
          </div>
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
