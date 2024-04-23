'use client'

import {FormControl, MenuItem, Select, SelectChangeEvent, TextField} from "@mui/material";
import {useEffect, useState} from "react";
import {createProcess} from "../client-api-helpers/process-helper";
import {getAgents} from "../client-api-helpers/machine-helper";

export interface ChooseAgentFormProps {
  machineUrl: string,
  // eslint-disable-next-line no-unused-vars
  handleSubmit: (proces_id: string) => void
}

export function ChooseAgentForm({handleSubmit, machineUrl}: ChooseAgentFormProps) {
  const [title, setTitle] = useState<string>("")
  const [agent, setAgent] = useState<string>("")
  const [agents, setAgents] = useState<string[]>([])

  const internalHandleSubmit = () => {
    createProcess(machineUrl, agent, title).then((process) => {
      handleSubmit(process?.process_id!)
    })
  }
  useEffect(() => {
    getAgents(machineUrl).then((agents) => {
      setAgents(agents)
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