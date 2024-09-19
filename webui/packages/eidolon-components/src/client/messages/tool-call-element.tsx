import React, { useState } from 'react';
import { ChevronDown, Circle, Wrench } from 'lucide-react';
import { ToolCallElement } from "../lib/display-elements.ts";
import { ChatDisplayElement } from "./chat-display-element.js";
import { EidolonMarkdown } from "./eidolon-markdown.js";
import styles from "./eidolon-events.module.css";

export interface ToolCallElementProps {
  machineUrl: string
  element: ToolCallElement
  agentName: string
}

export const ToolCall: React.FC<ToolCallElementProps> = ({ machineUrl, element, agentName }) => {
  const [expanded, setExpanded] = useState(false);

  const handleExpandClick = () => {
    setExpanded(!expanded);
  };

  return (
    <div className="mt-2 mb-2 border border-gray-200 rounded-md">
      <div
        className="flex items-center justify-between p-2 cursor-pointer"
        onClick={handleExpandClick}
      >
        <div className="flex items-center">
          {element.is_agent
            ? <img src="/img/eidolon_with_gradient.png" alt="Agent" className="w-6 h-6 rounded-full" />
            : <div className="w-6 h-6 bg-gray-200 rounded-full flex items-center justify-center">
                <Wrench size={16} />
              </div>
          }
          <div className="ml-2">m
            <div className="text-sm font-medium">{element.is_agent ? `${element.title} Agent` : element.title}</div>
            <div className="text-xs text-gray-500">{element.sub_title}</div>
          </div>
        </div>
        <div className="flex items-center">
          {element.is_active && (
            <Circle className="w-4 h-4 text-blue-500 animate-pulse mr-2" />
          )}
          <ChevronDown
            className={`transform transition-transform duration-200 ${expanded ? 'rotate-180' : ''}`}
          />
        </div>
      </div>
      {expanded && (
        <div className="p-4 border-t border-gray-200">
          <h6 className="text-sm font-semibold mb-2">Input:</h6>
          <div className={styles[`chat-indent`]}>
            <EidolonMarkdown machineUrl={machineUrl}>
              {'```json\n' + JSON.stringify(element.arguments, undefined, "  ") + "\n```"}
            </EidolonMarkdown>
          </div>
          <hr className="my-4" />
          <h6 className="text-sm font-semibold mb-2">Output:</h6>
          {element.children.map((child, index) => {
            if (index < element.children.length - 1 || child.type !== "success") {
              return (
                <ChatDisplayElement
                  userImage={undefined}
                  userName={undefined}
                  machineUrl={machineUrl}
                  key={index}
                  rawElement={child}
                  topLevel={false}
                  agentName={agentName}
                />
              );
            }
            return null;
          })}
        </div>
      )}
    </div>
  );
};
