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
import {useProcesses} from "@eidolon/components";
import {TOP_BAR_DESKTOP_HEIGHT, TOP_BAR_MOBILE_HEIGHT} from "@/layout/config";
import {useOnMobile} from "@/hooks/index";

export interface DevProcessListWithAddProps {
  app: EidolonApp
}

export const DevProcessListWithAdd = ({app}: DevProcessListWithAddProps) => {
  const machineURL = app.location
  const {updateProcesses} = useProcesses()
  const [createProcessOpen, setCreateProcessOpen] = useState(false)
  const router = useRouter()
  const pathname = usePathname()
  const onMobile = useOnMobile();

  const addClicked = () => {
    if (app.type === 'copilot') {
      const options = app.params as CopilotParams
      createProcess(machineURL, options.agent, options.newItemText || "New Chat").then((process) => {
        if (process) {
          router.push(`/eidolon-apps/${app.path}/${process!.process_id}`)
        }
      }).then(() => updateProcesses(machineURL))
    } else {
      setCreateProcessOpen(true)
    }
  }

  return (
    <Box sx={{overflow: 'auto', height: '100%'}}>
      <Toolbar sx={{height: onMobile ? TOP_BAR_MOBILE_HEIGHT : TOP_BAR_DESKTOP_HEIGHT}}/>
      <Box height={`calc(100% - ${onMobile ? TOP_BAR_MOBILE_HEIGHT : TOP_BAR_DESKTOP_HEIGHT})`}>
        <List>
          <ListItem disablePadding onClick={addClicked}>
            <ListItemButton>
              <ListItemIcon>
                <AddCircleOutline/>
              </ListItemIcon>
              <ListItemText primary={app.params.addBtnText || "Add Chat"}/>
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
    </Box>
  )
}
