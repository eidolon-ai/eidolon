'use client'

import {Button, Dialog, DialogActions, DialogContent, DialogTitle, Divider, Paper, PaperProps, Typography} from "@mui/material";
import * as React from "react";
import {usePathname, useRouter} from "next/navigation";
import {ChooseAgentForm, getAppPathFromPath} from "@eidolon/components";

export function StartProgramDialog({agents, open, onClose, machineUrl}: { agents: string[], machineUrl: string, open: boolean, onClose: (wasCanceled: boolean) => void }) {
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
          agents={agents}
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