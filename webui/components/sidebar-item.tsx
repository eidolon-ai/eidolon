'use client'

import {Chat} from "@/lib/types";
import {usePathname, useRouter} from "next/navigation";
import * as React from "react";
import {
  Collapse,
  IconButton,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemSecondaryAction,
  ListItemText
} from "@mui/material";
import {UnfoldLess, UnfoldMore} from "@mui/icons-material";
import DeleteIcon from '@mui/icons-material/Delete';

export function SidebarItem({chat, handleDelete}: {
  chat: Chat,
  handleDelete: (agentName: string, process_id: string) => void
}) {
  const pathname = usePathname()
  const router = useRouter()
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
        selected={pathname === chat.path}
      >
        <ListItemIcon onClick={handleExpandClick}>
          {chat.children?.length && (
            open ? <UnfoldLess sx={{width: 24}}/> : <UnfoldMore sx={{width: 24}}/>
          )}
        </ListItemIcon>
        <ListItemText
          onClick={() => {
            router.push(chat.path)
          }}
          primary={`${chat.title}`}/>
        <ListItemSecondaryAction
          // only show on hover
          sx={{visibility: "hidden"}}
          onClick={(event) => {
            handleDelete(chat.agent, chat.process_id)
            event.stopPropagation()
          }}
        >
          <IconButton edge={"end"}><DeleteIcon/></IconButton>
        </ListItemSecondaryAction>
      </ListItemButton>
      {chat.children?.length && (
        <Collapse in={open} timeout="auto" unmountOnExit>
          <List component="div" disablePadding>
            {chat.children!.map(
              child => (<SidebarItem key={child.process_id} handleDelete={handleDelete} chat={child}/>))}
          </List>
        </Collapse>
      )}
    </ListItem>
  )
}