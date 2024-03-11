// noinspection JSUnusedGlobalSymbols

'use client'

import {Chat} from "../lib/types.js";
import {Box, Button, List, ListItem, ListItemText, ListSubheader} from "@mui/material";
import * as React from "react";
import {useEffect, useState} from "react";
import {ProcessSummary} from "./process-summary.js";
import {deleteChat, getChatsForUI} from "./process-list-helpers.js";

export interface ProcessListProps {
  isSelected: (chat: Chat) => boolean
  selectChat: (chat: Chat) => void
  goHome: () => void
  createChat: () => void
}

export function ProcessList({isSelected, selectChat, goHome, createChat}: ProcessListProps) {
  const [dataByDate, setDataByDate] = useState<Record<string, Chat[]>>({})
  const handleDelete = (chat: Chat) => {
    const process_id = chat.process_id
    deleteChat(process_id).then(() => {
      if (isSelected(chat)) {
        // get the previous item in the list from the current process_id and navigate to it by iterating through the
        // dataByDate object and then each array of chats, keeping the previous item in a variable
        let previousItem: Chat | undefined
        let replaceWithNextItem = false
        for (const [_date, chats] of Object.entries(dataByDate)) {
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
    }).then(() => getChatsForUI().then(chats => setDataByDate(chats)))
  }

  useEffect(() => {
    getChatsForUI().then(chats => setDataByDate(chats))
    return () => {
    }
  }, []);

  let listComponents = (
    <List>
      <ListItem>
        <ListItemText primary="No chat history"/>
      </ListItem>
    </List>

  )

  if (Object.keys(dataByDate).length) {
    listComponents = (
      <List>
        {Object.entries(dataByDate).map(([date, chats]) => {
          return (
            <Box key={date}>
              <ListSubheader>{date}</ListSubheader>
              {chats.map(chat => {
                return (
                  <ProcessSummary
                    key={chat.id}
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
    <>
      <Button
        variant={"outlined"}
        sx={{margin: '8px 16px 16px 16px '}}
        // disabled={isCreatePending}
        onClick={(event) => {
          createChat()
          // router.push("?modal=true")
          event.preventDefault()
          event.stopPropagation()
        }}
      >
        New Chat
      </Button>
      <Box sx={{overflow: 'auto'}}>
        {listComponents}
      </Box>
    </>
  )
}

