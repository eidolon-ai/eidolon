'use client'

import {CopilotParams, createProcess, EidolonApp, ProcessList} from "@eidolon/components";
import {usePathname, useRouter} from "next/navigation";
import {ProcessStatus} from "@eidolon/client";
import * as React from "react";
import {useState} from "react";
import {StartProgramDialog} from "../app/eidolon-apps/dev-tool/components/start-program-dialog";
import {Box, Divider, ListItem, ListItemButton, ListItemIcon, ListItemText, Toolbar} from "@mui/material";
import List from "@mui/material/List";
import {AddCircleOutline} from "@mui/icons-material";
import {useProcesses} from "../../../packages/eidolon-components/src/hooks/processes_context";

export interface DevProcessListWithAddProps {
  app: EidolonApp
}

export const DevProcessListWithAdd = ({app}: DevProcessListWithAddProps) => {
  const machineURL = app.location
  const {updateProcesses} = useProcesses(machineURL)
  const [createProcessOpen, setCreateProcessOpen] = useState(false)
  const router = useRouter()
  const pathname = usePathname()

  const addClicked = () => {
    if (app.type === 'copilot') {
      const options = app.params as CopilotParams
      createProcess(machineURL, options.agent, "New Chat").then((process) => {
        if (process) {
          router.push(`/eidolon-apps/${app.path}/${process!.process_id}`)
        }
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
