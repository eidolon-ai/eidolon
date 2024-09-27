import {AgentStartElement} from "../lib/display-elements.js";
import {ChatDisplayElement} from "./chat-display-element.js";

export interface ToolCallElementProps {
  element: AgentStartElement
  agentName: string
  goToProcess: (processId: string) => void;
}

export const AgentCall = ({element, agentName, goToProcess}: ToolCallElementProps) => {
  return (
    <div className={"flex flex-col border-r-4 rounded-xl py-4 pr-2 gap-4 leading-normal"}>
      {element.children.map((child, index) => {
          if (index < element.children.length - 1 || child.type != "success") {
            return <ChatDisplayElement userImage={undefined} userName={undefined} key={index} rawElement={child} topLevel={true} agentName={agentName}
                                       depth={0} goToProcess={goToProcess}
            />
          }
        }
      )}
    </div>
  )
}
