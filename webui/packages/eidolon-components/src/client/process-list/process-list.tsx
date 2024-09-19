'use client'

import React, { useEffect } from 'react';
import { ProcessSummary } from "./process-summary.tsx";
import { deleteProcess } from "../client-api-helpers/process-helper.ts";
import { ProcessStatus } from "@eidolon-ai/client";
import { useProcesses } from "../hooks/processes_context.tsx";

export interface ProcessListProps {
  isSelected: (chat: ProcessStatus) => boolean;
  selectChat: (chat: ProcessStatus) => void;
  goHome: () => void;
  machineURL: string;
}

export function ProcessList({ machineURL, isSelected, selectChat, goHome }: ProcessListProps) {
  const { processes, updateProcesses, fetchError } = useProcesses();

  useEffect(() => {
    updateProcesses(machineURL).then(() => {});
  }, [machineURL]);

  const handleDelete = (chat: ProcessStatus) => {
    const process_id = chat.process_id;
    deleteProcess(chat.machine, process_id).then(() => {
      if (isSelected(chat)) {
        let previousItem: ProcessStatus | undefined;
        let replaceWithNextItem = false;
        for (const [_, chats] of Object.entries(processes)) {
          for (const chat of chats) {
            if (replaceWithNextItem) {
              return selectChat(chat);
            }
            if (chat.process_id === process_id) {
              if (previousItem) {
                return selectChat(previousItem);
              } else {
                replaceWithNextItem = true;
              }
            }
            previousItem = chat;
          }
        }
        goHome();
      }
    }).then(() => updateProcesses(machineURL));
  };

  let listComponents;

  if (fetchError) {
    listComponents = (
      <ul className="list-none p-0">
        <li className="p-4">
          <p className="text-red-500">Failed to fetch chat history</p>
        </li>
      </ul>
    );
  } else if (Object.keys(processes).length === 0) {
    listComponents = (
      <ul className="list-none p-0">
        <li className="p-4">
          <p className="text-gray-500">No chat history</p>
        </li>
      </ul>
    );
  } else {
    listComponents = (
      <ul className="list-none p-0 h-full">
        {Object.entries(processes).map(([date, chats]) => (
          <li key={date} className="mb-4">
            <h3 className="text-sm font-semibold text-gray-500 sticky top-0 p-2 underline">{date}</h3>
            <ul className="list-none p-0">
              {chats.map(chat => (
                <ProcessSummary
                  key={chat.process_id}
                  chat={chat}
                  handleDelete={handleDelete}
                  isSelected={isSelected}
                  selectChat={selectChat}
                />
              ))}
            </ul>
          </li>
        ))}
      </ul>
    );
  }

  return (
    <div className="overflow-auto">
      {listComponents}
    </div>
  );
}