'use client'

import {Chat} from "../lib/types.js";
import * as React from "react";
import {Collapse, IconButton, List, ListItem, ListItemButton, ListItemIcon, ListItemSecondaryAction, ListItemText} from "@mui/material";
import {UnfoldLess, UnfoldMore} from "@mui/icons-material";
import {Delete} from '@mui/icons-material';

export interface ProcessSummaryProps {
  chat: Chat,
  handleDelete: (chat: Chat) => void
  isSelected: (chat: Chat) => boolean
  selectChat: (chat: Chat) => void
}

export function ProcessSummary({chat, handleDelete, isSelected, selectChat}: ProcessSummaryProps) {
  const [open, setOpen] = React.useState(false);

  const handleExpandClick = (event: { stopPropagation: () => void; }) => {
    setOpen(!open);
    console.log("clicked")
    event.stopPropagation()
  };

  return (
    <ListItem
      disablePadding={true}
      sx={{"&:hover .MuiListItemSecondaryAction-root": {visibility: "inherit"}}}
    >
      <ListItemButton
        key={chat?.id}
        selected={isSelected(chat)}
      >
        <ListItemIcon onClick={handleExpandClick}>
          {chat.children?.length && (
            open ? <UnfoldLess sx={{width: 24}}/> : <UnfoldMore sx={{width: 24}}/>
          )}
        </ListItemIcon>
        <ListItemText
          onClick={() => {
            selectChat(chat)
          }}
          primary={`${chat.title}`}/>
        <ListItemSecondaryAction
          // only show on hover
          sx={{visibility: "hidden"}}
          onClick={(event) => {
            handleDelete(chat)
            event.stopPropagation()
          }}
        >
          <IconButton edge={"end"}><Delete/></IconButton>
        </ListItemSecondaryAction>
      </ListItemButton>
      {chat.children?.length && (
        <Collapse in={open} timeout="auto" unmountOnExit>
          <List component="div" disablePadding>
            {chat.children!.map(
              child => (
                <ProcessSummary
                  key={child.process_id}
                  handleDelete={handleDelete}
                  chat={child}
                  isSelected={isSelected}
                  selectChat={selectChat}
                />
              ))}
          </List>
        </Collapse>
      )}
    </ListItem>
  )
}