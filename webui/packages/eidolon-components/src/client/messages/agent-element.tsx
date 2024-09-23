import {AgentStartElement} from "../lib/display-elements.js";
import {ChatDisplayElement} from "./chat-display-element.js";

export interface ToolCallElementProps {
  machineUrl: string
  element: AgentStartElement
  agentName: string
}

export const AgentCall = ({machineUrl, element, agentName}: ToolCallElementProps) => {
  return (
    <div className={"flex flex-col border-r-4 rounded-xl py-4 pr-2 gap-4 leading-normal"}>
      {element.children.map((child, index) => {
          if (index < element.children.length - 1 || child.type != "success") {
            return <ChatDisplayElement userImage={undefined} userName={undefined} machineUrl={machineUrl} key={index} rawElement={child} topLevel={true} agentName={agentName}
                                       depth={0}
            />
          }
        }
      )}
    </div>
  )
}
