'use client'

import {AgentInputForm} from "@/components/agent-input/agent-input-form";
import * as React from "react";
import {useEffect, useState} from "react";
import {EidolonClient, OperationInfo, ProcessState} from "@/lib/types";
import ArrowCircleUpRoundedIcon from '@mui/icons-material/ArrowCircleUpRounded';
import AddCircleRoundedIcon from '@mui/icons-material/AddCircleRounded';
import RemoveCircleRoundedIcon from '@mui/icons-material/RemoveCircleRounded';
import {Button, Paper, Skeleton} from "@mui/material";
import CancelRoundedIcon from '@mui/icons-material/CancelRounded';
import {ButtonScrollToBottom} from "@/components/button-scroll-to-bottom";

interface AgentProcessProps {
  agent: string
  processState?: ProcessState
  handleAction: (operation: OperationInfo, data: Record<string, any>) => void
  handleCancel: () => void
}

const eidolonServer = process.env.EIDOLON_SERVER
export function AgentProcess({agent, processState, handleAction, handleCancel}: AgentProcessProps) {
  const [bigForm, setBigForm] = useState(false)

  const [client] = useState(new EidolonClient(eidolonServer || "http://localhost:8080"))
  const [operations, setOperations] = useState<OperationInfo[]>([])
  useEffect(() => {
    if (processState?.available_actions) {
      client.getActionsForDisplay(agent, processState?.available_actions).then(programs => {
        setOperations(programs)
      })
    }
    return () => {
    }
  }, [client, agent, processState])

  const handleSubmit = (formJson: Record<string, any>) => {
    handleAction(formJson.operation as OperationInfo, formJson.data)
  }

  let content = (
    <AgentInputForm handleSubmit={handleSubmit} operations={operations} isProgram={false}/>
  )

  let button = (
    <Button form="agent-input-form" variant={'text'} type={"submit"}><ArrowCircleUpRoundedIcon style={{fontSize: 36}}/></Button>
  )
  if (processState?.state === "initialized") {
    // do nothing???
  } else if (processState?.state === "processing") {
    content = (
      <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
        <h2>Running...</h2>
      </div>
    )
    button = (
      <Button variant={'text'} onClick={handleCancel}><CancelRoundedIcon style={{fontSize: 36}}/></Button>
    )
  } else if (!processState) {
    content = (
      <div>
        <Skeleton variant="rectangular" height={60}/>
        <Skeleton variant="text" height={60}/>
      </div>
    )
    button = <Skeleton variant="circular" width={36} height={36}/>
  } else if (processState?.state === 'http_error') {
    content = (
      <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
        <h2>Error</h2>
        The process has encountered an error and can no longer accept input.<br/>
        Error: {processState?.error}
      </div>

    )
    button = <span></span>
  } else if (processState?.available_actions?.length === 0) {
    content = (
      <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
        <h3>Terminated</h3>
        The process has terminated and can no longer accept input.
      </div>

    )
    button = <span></span>
  }

  const toggleFormSize = () => {
    setBigForm(!bigForm)
  }

  return (
    <>
      <Paper elevation={6} sx={{
        maxHeight: !bigForm ? '260px' : '70vh',
        minHeight: !bigForm ? '260px' : '70vh',
        width: '100%',
        padding: '16px 8px 12px 16px',
        marginBottom: '16px'
      }}>
        <div style={{textAlign: "center", width: "100%", marginTop: "-48px", height: "48px"}}>
          <ButtonScrollToBottom/>
        </div>
        <div style={{display: 'flex', width: '100%', height: '100%'}}>
          <div style={{flexGrow: '1', overflowY: 'scroll'}}>
            {content}
          </div>
          <div
            style={{
              verticalAlign: 'bottom',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between'
            }}>
            {bigForm && (<Button onClick={toggleFormSize} variant={'text'}><RemoveCircleRoundedIcon
              style={{fontSize: 18}}/></Button>)
            }
            {!bigForm &&
              (<Button onClick={toggleFormSize} variant={'text'}><AddCircleRoundedIcon
                style={{fontSize: 18}}/></Button>)
            }
            {button}
          </div>
        </div>
      </Paper>
    </>
  )
}
