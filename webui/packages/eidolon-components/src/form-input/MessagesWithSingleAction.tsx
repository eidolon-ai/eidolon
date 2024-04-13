'use client'

import {Box, Button, Divider, Paper, Skeleton, TextField, Typography} from "@mui/material";
import {ArrowCircleUpRounded, CancelRounded} from "@mui/icons-material";
import {useState} from "react";
import {useProcessEvents} from "../hooks/useProcessEvents";
import {EidolonEvents} from "../messages/eidolon-events";
import Recorder from "../audio/Recorder";
import {ChooseLLMElement} from "../messages/choose-llm-element";
import {ButtonScrollToBottom} from "./button-scroll-to-bottom";
import {executeOperation} from "../client-api-helpers/process-event-helper";
import {useProcesses} from "../hooks/process_context";
import {useSupportedLLMsOnOperation} from "../hooks/useSupportedLLMsOnOperation";
import {OperationInfo} from "@eidolon/client";

export interface MessagesWithActionProps {
  supportedLLMs: string[] | undefined,
  operation: OperationInfo,
  machineUrl: string
  agent: string
  processId: string
  operationName: string
  titleOperationName?: string
  inputLabel: string
  allowSpeech?: boolean
  speechAgent?: string
  speechOperation?: string
}

export function MessagesWithSingleAction({
                                           supportedLLMs,
                                           operation,
                                           machineUrl,
                                           agent,
                                           processId,
                                           operationName,
                                           titleOperationName,
                                           inputLabel,
                                           allowSpeech,
                                           speechAgent,
                                           speechOperation
                                         }: MessagesWithActionProps) {
  const {selectedLLM, setSelectedLLM} = useSupportedLLMsOnOperation(operation)
  const {
    processState,
    elementsAndLookup,
    executeAction,
    handleCancel
  } = useProcessEvents(machineUrl, agent, processId)
  const [input, setInput] = useState("")
  const {updateProcesses} = useProcesses()

  const handleKeyDown = async (
    event: React.KeyboardEvent
  ) => {
    if (event.key === 'Enter') {
      if (event.shiftKey) {
        // Handle Shift+Enter key combination
        // Add a new line to the TextField value
        event.preventDefault();
        let {value, selectionStart, selectionEnd} = event.target as HTMLInputElement | HTMLTextAreaElement;
        if (selectionStart == null) {
          selectionStart = 0;
        }
        if (selectionEnd == null) {
          selectionEnd = value.length;
        }

        (event.target as HTMLInputElement | HTMLTextAreaElement).value = value.slice(0, selectionStart) + '\n' + value.slice(selectionEnd);
      } else {
        // Handle Enter key press
        event.preventDefault();
        await doAction()
      }
    }
  }

  async function doAction() {
    let payload: any = input

    if (supportedLLMs && supportedLLMs.length > 0) {
      payload = {
        body: input,
        execute_on_cpu: selectedLLM
      }
    }

    if (processState?.state === "initialized" && titleOperationName) {
      // generate a title
      await executeOperation(machineUrl, agent, titleOperationName, processId, payload)
      updateProcesses(machineUrl).then()
    }
    setInput("")
    await executeAction(machineUrl, agent, operationName, payload)
  }

  let content = (
    <div style={{display: "flex", flexDirection: "row", width: "100%"}}>
      <TextField
        multiline
        variant={"standard"}
        label={inputLabel}
        fullWidth
        maxRows={10}
        sx={{margin: "8px 0px 8px 8px"}}
        value={input}
        onKeyDown={handleKeyDown}
        onChange={(e) => setInput(e.target.value)}
        inputProps={{"x-webkit-speech": "x-webkit-speech"}}
      />
      {allowSpeech && (<Recorder machineUrl={machineUrl} agent={speechAgent!} operation={speechOperation!} process_id={processId} setText={(text) => {
        setInput(text)
      }}/>)}
    </div>
  )
  let button = (
    <Button
      variant={'text'}
      onClick={doAction}><ArrowCircleUpRounded
      style={{fontSize: 36}}
      sx={{padding: "0px"}}
    /></Button>
  )

  if (processState?.state === "initialized") {
    // do nothing???
  } else if (processState?.state === "processing") {
    button = (
      <Button variant={'text'} onClick={handleCancel}><CancelRounded style={{fontSize: 36}}/></Button>
    )
  } else if (!processState) {
    content = (
      <Skeleton variant="text" height={"64px"} width={"100%"} sx={{marginRight: "20px"}}/>
    )
    button = (
      <div style={{display: "flex", alignItems: "center"}}>
        <Skeleton variant="circular" width={36} height={36} sx={{marginRight: "12px"}}/>
      </div>
    )
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

  return (
    <Box sx={{
      height: '100%',
      width: '65vw',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'space-between',
      alignItems: 'center',
      overflow: "hidden"
    }}>
      <EidolonEvents agentName={agent} elementsAndLookup={elementsAndLookup}
      />
      <div style={{textAlign: "right", width: "100%", height: "32px", marginRight: "35px"}}>
        <ButtonScrollToBottom/>
      </div>
      <Paper
        sx={{
          width: "100%",
          marginBottom: "16px",
          paddingTop: "8px",
          paddingLeft: "16px",
          paddingRight: "8px",
          paddingBottom: "8px",
          borderRadius: "16px",
          borderStyle: "solid",
          borderColor: "lightblue",
          display: "flex",
          flexDirection: "column",
        }}
      >
        <div style={{display: "flex", flexDirection: "row", justifyContent: "space-between", marginLeft: "8px", marginRight: "8px"}}>
          <ChooseLLMElement supportedLLMs={supportedLLMs} selectedLLM={selectedLLM} setSelectedLLM={setSelectedLLM}
          />
          <Typography sx={{marginBottom: "6px"}} alignSelf={"end"} variant={"caption"}>Press <b>Shift-Enter</b> to add a line</Typography>
        </div>
        <Divider sx={{marginTop: "-1px"}}/>
        <div style={{width: "100%", display: "flex", flexDirection: "row"}}>
          {content}
          {button}
        </div>
      </Paper>
    </Box>
  )
}
