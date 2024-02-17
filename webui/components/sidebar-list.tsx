'use client'

import {deleteChat, getChatsForUI} from '@/app/api/chat/route'
import {Chat} from "@/lib/types";
import {Box, Button, List, ListItem, ListItemText, ListSubheader} from "@mui/material";
import * as React from "react";
import {useEffect, useState} from "react";
import {SidebarItem} from "@/components/sidebar-item";
import {usePathname, useRouter} from "next/navigation";
import {StartProgramDialog} from "@/components/agent-input/start-program-dialog";

export function SidebarList() {
  const pathname = usePathname()
  const router = useRouter()
  const [dataByDate, setDataByDate] = useState<Record<string, Chat[]>>({})
  const handleDelete = (agentName: string, process_id: string) => {
    deleteChat(agentName, process_id).then(() => {
      if (pathname === `/chat/${process_id}`) {
        // get the previous item in the list from the current process_id and navigate to it by iterating through the
        // dataByDate object and then each array of chats, keeping the previous item in a variable
        let previousItem: Chat | undefined
        let replaceWithNextItem = false
        for (const [date, chats] of Object.entries(dataByDate)) {
          for (const chat of chats) {
            if (replaceWithNextItem) {
              return router.replace(`/chat/${chat.process_id}`)
            }
            if (chat.process_id === process_id) {
              if (previousItem) {
                return router.replace(`/chat/${previousItem.process_id}`)
              } else {
                replaceWithNextItem = true
              }
            }
            previousItem = chat
          }
        }
        return router.replace("/")
      }
    }).then(() => getChatsForUI().then(chats => setDataByDate(chats)))
  }

  useEffect(() => {
    console.log("here")
    getChatsForUI().then(chats => setDataByDate(chats))
    return () => {
    }
  }, []);

  const [open, setOpen] = React.useState(false)

  const onDialogClose = (wasCanceled: boolean) => {
    setOpen(false)
    getChatsForUI().then(chats => setDataByDate(chats))
  }

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
                  <SidebarItem key={chat.id} chat={chat} handleDelete={handleDelete}/>
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
          // todo -- change to create a new pid for the
          setOpen(true)
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
      <StartProgramDialog open={open} onClose={onDialogClose}/>
    </>
  )
}

