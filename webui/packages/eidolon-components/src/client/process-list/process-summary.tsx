'use client'

import {Collapse, IconButton, List, ListItem, ListItemButton, ListItemIcon, ListItemSecondaryAction, ListItemText, Typography} from "@mui/material";
import {UnfoldLess, UnfoldMore} from "@mui/icons-material";
import {Delete} from '@mui/icons-material';
import {ProcessStatus} from "@eidolon/client";
import {ProcessStatusWithChildren} from "../client-api-helpers/process-helper.ts";
import {useState} from "react";

export interface ProcessSummaryProps {
  chat: ProcessStatusWithChildren,
  // eslint-disable-next-line no-unused-vars
  handleDelete: (chat: ProcessStatus) => void
  // eslint-disable-next-line no-unused-vars
  isSelected: (chat: ProcessStatus) => boolean
  // eslint-disable-next-line no-unused-vars
  selectChat: (chat: ProcessStatus) => void
}

export function ProcessSummary({chat, handleDelete, isSelected, selectChat}: ProcessSummaryProps) {
  const [open, setOpen] = useState(false);

  const handleExpandClick = (event: { stopPropagation: () => void; }) => {
    setOpen(!open);
    event.stopPropagation()
  };

  return (
    <ListItem
      dense
      disablePadding={true}
      sx={{"&:hover .MuiListItemSecondaryAction-root": {visibility: "inherit"}, "flexDirection": "column", alignItems: "baseline"}}
    >
      <ListItemButton
        key={chat?.process_id}
        selected={isSelected(chat)}
        sx={{paddingTop: 0, paddingBottom:0, width: "100%"}}
      >
        <ListItemIcon onClick={handleExpandClick} sx={{minWidth: "28px"}}>
          {chat.children?.length && (
            open ? <UnfoldLess sx={{width: 24}}/> : <UnfoldMore sx={{width: 24}}/>
          )}
        </ListItemIcon>
        <ListItemText
          onClick={() => {
            selectChat(chat)
          }}
          >
          <Typography fontSize={"0.9em"}>{chat.title}</Typography>
        </ListItemText>
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
        <Collapse in={open} timeout="auto" unmountOnExit sx={{width: "100%"}}>
          <List component="ul" disablePadding>
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