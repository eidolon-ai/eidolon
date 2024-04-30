'use client'

import {AgentInputForm} from "./agent-input-form";
import {useState} from "react";
import {OperationInfo, ProcessStatus} from "@eidolon/client";
import {AddCircleRounded, ArrowCircleUpRounded, CancelRounded, RemoveCircleRounded} from '@mui/icons-material';
import {Button, Paper, Skeleton} from "@mui/material";
import {ButtonScrollToBottom} from "./button-scroll-to-bottom";

interface AgentProcessProps {
  operations: OperationInfo[]
  processState?: ProcessStatus
  // eslint-disable-next-line no-unused-vars
  handleAction: (machine: string, agent: string, operation: string, data: any) => void
  handleCancel: () => void
}

export function AgentProcess({operations, processState, handleAction, handleCancel}: AgentProcessProps) {
  const [bigForm, setBigForm] = useState(false)
  const handleSubmit = (formJson: Record<string, any>) => {
    let operation = formJson.operation as OperationInfo;
    handleAction(operation.machine, operation.agent, operation.name, formJson.data)
  }

  let content = (
    <AgentInputForm handleSubmit={handleSubmit} operations={operations} isProgram={false} processState={processState}/>
  )

  let button = (
    <Button form="agent-input-form" variant={'text'} type={"submit"}><ArrowCircleUpRounded style={{fontSize: 36}}/></Button>
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
      <Button variant={'text'} onClick={handleCancel}><CancelRounded style={{fontSize: 36}}/></Button>
    )
  } else if (!processState) {
    content = (
      <div>
        <Skeleton variant="rectangular" height={60}/>
        <Skeleton variant="text" height={60}/>
      </div>
    )
    button = <Skeleton variant="circular" width={36} height={36}/>
  } else if ((processState?.state === 'http_error' || processState?.state === 'error' || processState?.state === 'unhandled_error') && processState?.available_actions?.length === 0) {
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
            {bigForm && (<Button onClick={toggleFormSize} variant={'text'}><RemoveCircleRounded
              style={{fontSize: 18}}/></Button>)
            }
            {!bigForm &&
              (<Button onClick={toggleFormSize} variant={'text'}><AddCircleRounded
                style={{fontSize: 18}}/></Button>)
            }
            {button}
          </div>
        </div>
      </Paper>
    </>
  )
}
