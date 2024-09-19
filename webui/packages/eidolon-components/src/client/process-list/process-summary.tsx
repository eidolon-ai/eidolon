import React, { useState } from 'react';
import { ChevronRight, ChevronDown, Trash2 } from 'lucide-react';
import { ProcessStatus } from "@eidolon-ai/client";
import { ProcessStatusWithChildren } from "../client-api-helpers/process-helper.ts";

interface ProcessSummaryProps {
  chat: ProcessStatusWithChildren;
  handleDelete: (chat: ProcessStatus) => void;
  isSelected: (chat: ProcessStatus) => boolean;
  selectChat: (chat: ProcessStatus) => void;
  depth?: number;
}

export function ProcessSummary({ chat, handleDelete, isSelected, selectChat, depth = 0 }: ProcessSummaryProps) {
  const [open, setOpen] = useState(false);

  const handleExpandClick = (event: React.MouseEvent) => {
    setOpen(!open);
    event.stopPropagation();
  };

  const handleDeleteClick = (event: React.MouseEvent) => {
    event.stopPropagation();
    handleDelete(chat);
  };

  return (
    <li className="w-full p-0">
      <div
        className={`group flex items-center w-full py-1 hover:bg-gray-100 transition-colors duration-200 ${isSelected(chat) ? 'bg-gray-100' : ''}`}
        onClick={() => selectChat(chat)}
      >
        {chat.children?.length ? (
          <button
            onClick={handleExpandClick}
            className="mr-2 text-gray-400 hover:text-gray-600 p-0"
          >
            {open ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
          </button>
        ) : (
          <div className="w-6 mr-2" /> // Placeholder for alignment
        )}
        <span className="text-sm text-gray-700 flex-grow">{chat.title}</span>
        {depth === 0 && (
          <button
            onClick={handleDeleteClick}
            className="text-gray-400 hover:text-gray-600 p-1 opacity-0 group-hover:opacity-100 transition-opacity duration-200"
          >
            <Trash2 size={16} />
          </button>
        )}
      </div>
      {chat.children?.length && open && (
        <ul className="pl-4 list-none p-0">
          {chat.children.map(child => (
            <ProcessSummary
              key={child.process_id}
              chat={child}
              handleDelete={handleDelete}
              isSelected={isSelected}
              selectChat={selectChat}
              depth={depth + 1}
            />
          ))}
        </ul>
      )}
    </li>
  );
}