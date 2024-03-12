'use client'

import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Divider,
  FormControl,
  MenuItem,
  Paper,
  PaperProps,
  Select,
  SelectChangeEvent,
  TextField,
  Typography
} from "@mui/material";
import * as React from "react";
import {useEffect, useState} from "react";
import Draggable from 'react-draggable';
import {EidolonClient} from "@/lib/types";
import {useRouter} from "next/navigation";
import {createPID} from "@/app/api/chat/messages/chatHelpers";

function PaperComponent(props: PaperProps) {
  return (
    <Draggable
      handle="#draggable-dialog-title"
      cancel={'[class*="MuiDialogContent-root"]'}
    >
      <Paper {...props} />
    </Draggable>
  );
}

export function StartProgramDialog({open, onClose}: { open: boolean, onClose: (wasCanceled: boolean) => void }) {
  const router = useRouter()
  const eidolonServer = process.env.EIDOLON_SERVER
  const [title, setTitle] = useState<string>("")
  const [agent, setAgent] = useState<string>("")

  const [agents, setAgents] = useState<string[]>([])
  useEffect(() => {
    const client = new EidolonClient(eidolonServer || "http://localhost:8080")
    client.getAgents().then(agents => {
      setAgents(agents)
      setAgent(agents[0])
    })
    return () => {
    }
  }, [])

  const handleCancel = () => {
    onClose(true);
  }

  const handleSubmit = () => {
    // todo -- handle title
    createPID(agent, title).then((process_id: string) => {
      onClose(false);
      router.push(`/chat/${process_id}`)
    })
  }

  return (
    <Dialog
      open={open}
      scroll={"paper"}
      PaperComponent={PaperComponent}
      keepMounted={true}
      PaperProps={{
        style: {width: '50%'}
      }}
    >
      <DialogTitle style={{cursor: 'move'}} id="draggable-dialog-title">
        Start a new chat
        <Typography variant={"body1"}>Choose the agent and then click Start.</Typography>
      </DialogTitle>
      <Divider/>
      <DialogContent>
        <form
          id={"start-program-form"}
          onSubmit={(event) => {
            event.preventDefault();
            handleSubmit()
          }}
        >
          <FormControl variant={"standard"} fullWidth={true}>
            <TextField
              sx={{marginBottom: '16px'}}
              label={"Title"}
              required={true}
              value={title}
              onChange={(event) => setTitle(event.target.value)}
            />
            <Select
              labelId={"op_label"}
              label={"Operation"}
              sx={{marginBottom: '16px'}}
              value={agent}
              onChange={(event: SelectChangeEvent<string>) => {
                setAgent(event.target.value)
              }}
            >
              {agents.map((agent, index) => (
                <MenuItem
                  key={index}
                  value={agent}
                >{agent}</MenuItem>
              ))}
            </Select>
          </FormControl>
        </form>
      </DialogContent>
      <DialogActions>
        <Button onClick={handleCancel}>Cancel</Button>
        <Button form="start-program-form" type="submit">Start</Button>
      </DialogActions>
    </Dialog>
  )
}

//updated envar