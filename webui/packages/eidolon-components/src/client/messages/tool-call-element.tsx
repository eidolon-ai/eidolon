'use client'

import React, {useState} from 'react';
import {Crosshair, LoaderCircle, Minus, Plus} from 'lucide-react';
import {AgentStartElement, ToolCallElement} from "../lib/display-elements.js";
import {ChatDisplayElement} from "./chat-display-element.js";
import {EidolonMarkdown} from "./eidolon-markdown.js";

export interface ToolCallElementProps {
  element: ToolCallElement;
  agentName: string;
  depth: number;
  goToProcess: (processId: string) => void;
}

export const ToolCall: React.FC<ToolCallElementProps> = ({element, agentName, depth, goToProcess}) => {
  const [expanded, setExpanded] = useState(false);

  const handleExpandClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    setExpanded(!expanded);
  };

  const handleTargetClick = (element: ToolCallElement) => {
    const agentChild = element.children.find((child) => child.type === "agent-start") as AgentStartElement
    if (agentChild) {
      goToProcess(agentChild.process_id);
    }
  }

  const getBgColor = (depth: number) => {
    const colors = ['bg-gray-50', 'bg-gray-100', 'bg-gray-200', 'bg-gray-300',
      'bg-blue-50', 'bg-blue-100', 'bg-blue-200', 'bg-blue-300',
      'bg-green-50', 'bg-green-100', 'bg-green-200', 'bg-green-300'];
    return colors[depth % colors.length];
  };

  const bgColor = getBgColor(depth);

  return (
    <div className={`mt-2 mb-2`}>
      <div
        className={`flex flex-col relative w-fit ${bgColor} border border-gray-200 border-solid rounded-md cursor-pointer hover:bg-opacity-80 transition-colors duration-200 ${
          expanded ? 'rounded-b-none border-b-0' : ''
        }`}
      >
        <div className="flex flex-row items-center">
          <div className="px-3 py-2 text-sm font-medium text-gray-700 whitespace-nowrap"
               onClick={handleExpandClick}
          >
            {element.is_agent && <span>{element.title}</span>}
            {!element.is_agent && <div><span>{element.sub_title || element.title}</span></div>}
          </div>
          <div className="flex items-center ml-2">
            {(element.is_active) && (
              <div className="w-5 h-5 rounded-full flex items-center justify-center mr-2 ">
                <LoaderCircle className="w-4 h-4 text-blue-500 text-center animate-spin [animation-duration:2s]"/>
              </div>
            )}
            <div
              className={`w-5 h-5 rounded-full bg-amber-300 flex items-center justify-center mr-1 opacity-65 ${element.is_agent ? '' : 'hidden'}`}
              onClick={() => handleTargetClick(element)}
            >
              <Crosshair className="w-4 h-4 text-black text-center"/>
            </div>
            <div
              className="w-5 h-5 rounded-full bg-green-400 flex items-center justify-center mr-2 opacity-65"
              onClick={handleExpandClick}
            >
              {expanded ? (
                <Minus className="w-4 h-4 text-black"/>
              ) : (
                <Plus className="w-4 h-4 text-black"/>
              )}
            </div>
          </div>
        </div>
        {expanded && <div className={`left-0 right-0 absolute h-[1px] bottom-[-1px] ${bgColor}`}/>}
      </div>

      {expanded && (
        <div className={`${bgColor} border border-gray-200 border-solid rounded-b-md overflow-hidden`}>
          <div className="p-4">
            {!element.is_agent && (
              <div>
                <h6 className="text-sm font-semibold mb-2">Input:</h6>
                <div className="pl-4 border-l-2 border-gray-300">
                  <EidolonMarkdown>
                    {'```json\n' + JSON.stringify(element.arguments, null, 2) + "\n```"}
                  </EidolonMarkdown>
                </div>
                <hr className="my-4"/>
                <h6 className="text-sm font-semibold mb-2">Output:</h6>
              </div>
            )}
            <div className="space-y-2">
              {element.children.map((child, index) => {
                if (index < element.children.length - 1 || child.type !== "success") {
                  return (
                    <ChatDisplayElement
                      key={index}
                      userImage={undefined}
                      userName={undefined}
                      rawElement={child}
                      topLevel={false}
                      agentName={agentName}
                      depth={depth + 1}
                      goToProcess={goToProcess}
                    />
                  );
                }
                return null;
              })}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};