'use client'

import {CopilotParams, createProcess, ProcessList} from "@eidolon/components";
import {usePathname, useRouter} from "next/navigation";
import {ProcessStatus} from "@eidolon/client";
import * as React from "react";
import {useState} from "react";
import {StartProgramDialog} from "../app/eidolon-apps/dev-tool/components/start-program-dialog";
import {Box, Divider, ListItem, ListItemButton, ListItemIcon, ListItemText, Toolbar} from "@mui/material";
import List from "@mui/material/List";
import {AddCircleOutline} from "@mui/icons-material";
import {useProcesses} from "@eidolon/components/src/hooks/process_context";
import {EidolonApp} from "@/utils/eidolon-apps";

export interface DevProcessListWithAddProps {
  machineURL: string
  app: EidolonApp
}

export const DevProcessListWithAdd = ({machineURL, app}: DevProcessListWithAddProps) => {
  const {updateProcesses} = useProcesses()
  const [createProcessOpen, setCreateProcessOpen] = useState(false)
  const router = useRouter()
  const pathname = usePathname()

  const addClicked = () => {
    if (app.type === 'copilot') {
      const options = app.params as CopilotParams
      createProcess(machineURL, options.agent, "New Chat").then((process) => {
        router.push(`/eidolon-apps/${app.path}/${process!.process_id}`)
      }).then(() => updateProcesses(machineURL))
    } else {
      setCreateProcessOpen(true)
    }
  }

  return (
    <Box sx={{overflow: 'auto'}}>
      <Toolbar/>
      <List>
        <ListItem disablePadding onClick={addClicked}>
          <ListItemButton>
            <ListItemIcon>
              <AddCircleOutline/>
            </ListItemIcon>
            <ListItemText primary={"Add Chat"}/>
          </ListItemButton>
        </ListItem>
      </List>
      <Divider/>
      <ProcessList
        machineURL={machineURL}
        isSelected={(process: ProcessStatus) => pathname.includes(process.process_id)}
        selectChat={(process: ProcessStatus) => {
          router.push(`/eidolon-apps/${app.path}/${process!.process_id}`)
        }}
        goHome={() => {
        }}
      />
      <StartProgramDialog machineUrl={machineURL} open={createProcessOpen} onClose={() => {
        setCreateProcessOpen(false)
      }}/>
    </Box>
  )
}
