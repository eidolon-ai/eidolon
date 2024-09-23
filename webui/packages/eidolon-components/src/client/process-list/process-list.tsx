// noinspection JSUnusedGlobalSymbols
'use client'

import {Box, List, ListItem, ListItemText, ListSubheader} from "@mui/material";
import {ProcessSummary} from "./process-summary.tsx";
import {deleteProcess} from "../client-api-helpers/process-helper.ts";
import {ProcessStatus} from "@eidolon-ai/client";
import {useProcesses} from "../hooks/processes_context.tsx";
import {useEffect} from "react";

export interface ProcessListProps {
  // eslint-disable-next-line no-unused-vars
  isSelected: (chat: ProcessStatus) => boolean
  // eslint-disable-next-line no-unused-vars
  selectChat: (chat: ProcessStatus) => void
  goHome: () => void
  machineURL: string
}

export function ProcessList({machineURL, isSelected, selectChat, goHome}: ProcessListProps) {
  const {processes, updateProcesses, fetchError} = useProcesses()

  useEffect(() => {
    updateProcesses(machineURL).then(() => {})
  }, [machineURL])

  const handleDelete = (chat: ProcessStatus) => {
    const process_id = chat.process_id
    deleteProcess(chat.machine, process_id).then(() => {
      if (isSelected(chat)) {
        // get the previous item in the list from the current process_id and navigate to it by iterating through the
        // dataByDate object and then each array of chats, keeping the previous item in a variable
        let previousItem: ProcessStatus | undefined
        let replaceWithNextItem = false
        for (const [_, chats] of Object.entries(processes)) {
          for (const chat of chats) {
            if (replaceWithNextItem) {
              return selectChat(chat)
            }
            if (chat.process_id === process_id) {
              if (previousItem) {
                return selectChat(previousItem)
              } else {
                replaceWithNextItem = true
              }
            }
            previousItem = chat
          }
        }
        goHome()
      }
    }).then(() => updateProcesses(machineURL))
  }

  let listComponents = (
    <List>
      <ListItem>
        <ListItemText primary="No chat history"/>
      </ListItem>
    </List>

  )

  if (fetchError) {
    listComponents = (
      <List>
        <ListItem>
          <ListItemText primary="Failed to fetch chat history"/>
        </ListItem>
      </List>
    )
  } else if (Object.keys(processes).length) {
    listComponents = (
      <List>
        {Object.entries(processes).map(([date, chats]) => {
          return (
            <Box key={date}>
              <ListSubheader>{date}</ListSubheader>
              {chats.map(chat => {
                return (
                  <ProcessSummary
                    key={chat.process_id}
                    chat={chat}
                    handleDelete={handleDelete}
                    isSelected={isSelected}
                    selectChat={selectChat}
                  />
                )
              })}
            </Box>
          )
        })}
      </List>
    )
  }

  return (
    <Box sx={{overflow: 'auto'}}>
      {listComponents}
    </Box>
  )
}

