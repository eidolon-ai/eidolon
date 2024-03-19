'use client'

import {Button, Dialog, DialogActions, DialogContent, DialogTitle, Divider, Paper, PaperProps, Typography} from "@mui/material";
import * as React from "react";
import Draggable from 'react-draggable';
import {usePathname, useRouter} from "next/navigation";
import {ChooseAgentForm, getAppPathFromPath} from "@eidolon/components";

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

export function StartProgramDialog({open, onClose, machineUrl}: { machineUrl: string, open: boolean, onClose: (wasCanceled: boolean) => void }) {
  const router = useRouter()
  const pathname = usePathname()

  const handleCancel = () => {
    onClose(true);
  }

  const handleSubmit = (processId: string) => {
    const appPath = getAppPathFromPath(pathname)
    if (appPath) {
      router.push(appPath  + `/${processId}`)
      onClose(false)
    }
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
        <ChooseAgentForm
          machineUrl={machineUrl}
          handleSubmit={handleSubmit}
          />
      </DialogContent>
      <DialogActions>
        <Button onClick={handleCancel}>Cancel</Button>
        <Button form="start-program-form" type="submit">Start</Button>
      </DialogActions>
    </Dialog>
  )
}