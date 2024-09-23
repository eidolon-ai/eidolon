'use client'

import {FormControl, MenuItem, Select, SelectChangeEvent, TextField} from "@mui/material";
import {useEffect, useState} from "react";
import {createProcess} from "../client-api-helpers/process-helper.ts";
import {getAgents} from "../client-api-helpers/machine-helper.ts";

export interface ChooseAgentFormProps {
  machineUrl: string,
  // eslint-disable-next-line no-unused-vars
  handleSubmit: (proces_id: string) => void
  defaultAgent?: string
}

export function ChooseAgentForm({handleSubmit, machineUrl, defaultAgent}: ChooseAgentFormProps) {
  const [title, setTitle] = useState<string>("New Conversation")
  const [agent, setAgent] = useState<string>(defaultAgent || "")
  const [agents, setAgents] = useState<string[]>([])

  const internalHandleSubmit = () => {
    if (!agent) {
      throw new Error("Agent is required")
    }
    createProcess(machineUrl, agent, title).then((process) => {
      handleSubmit(process?.process_id!)
    })
  }
  useEffect(() => {
    getAgents(machineUrl).then((agents) => {
      setAgents(agents)
      if (agents.length > 0 && !agent && agents[0]) {
        setAgent(agents[0])
      }
    }).catch(() => {
      // ignore
    })
  }, [machineUrl]);

  return (
    <form
      id={"start-program-form"}
      onSubmit={(event) => {
        event.preventDefault();
        internalHandleSubmit()
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
  )
}