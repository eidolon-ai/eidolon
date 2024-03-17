'use client'

import * as React from "react";
import {Collapse, IconButton, List, ListItem, ListItemButton, ListItemIcon, ListItemSecondaryAction, ListItemText} from "@mui/material";
import {UnfoldLess, UnfoldMore} from "@mui/icons-material";
import {Delete} from '@mui/icons-material';
import {ProcessStatus} from "@eidolon/client";
import {ProcessStatusWithChildren} from "../client-api-helpers/process-helper.js";

export interface ProcessSummaryProps {
  chat: ProcessStatusWithChildren,
  handleDelete: (chat: ProcessStatus) => void
  isSelected: (chat: ProcessStatus) => boolean
  selectChat: (chat: ProcessStatus) => void
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
        key={chat?.process_id}
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