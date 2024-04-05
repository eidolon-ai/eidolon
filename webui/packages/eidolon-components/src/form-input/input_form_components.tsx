import {Badge, Button, IconButton, Skeleton, TextField} from "@mui/material";
import Recorder from "../audio/Recorder";
import {ArrowCircleUpRounded, CancelRounded} from "@mui/icons-material";
import {CopilotParams} from "../lib/util";
import {useState} from "react";
import {FileUpload} from "../file-upload/FileUpload";
import {FileHandle} from "@eidolon/client";

export function ProcessTerminated() {
  return (
    <div style={{width: "100%", display: "flex", flexDirection: "row"}}>
      <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
        <h3>Terminated</h3>
        The process has terminated and can no longer accept input.
      </div>
    </div>
  )
}

export function ProcessError({error}: { error: string }) {
  return (
    <div style={{width: "100%", display: "flex", flexDirection: "row"}}>
      <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
        <h2>Error</h2>
        The process has encountered an error and can no longer accept input.<br/>
        Error: {error}
      </div>
    </div>
  )
}

export function ProcessLoading() {
  return (
    <div style={{width: "100%", display: "flex", flexDirection: "row"}}>
      <Skeleton variant="text" height={"64px"} width={"100%"} sx={{marginRight: "20px"}}/>
      <div style={{display: "flex", alignItems: "center"}}>
        <Skeleton variant="circular" width={36} height={36} sx={{marginRight: "12px"}}/>
      </div>
    </div>
  )
}

interface CopilotInputFormProps {
  machineUrl: string
  processId: string
  isProcessing: boolean
  copilotParams: CopilotParams
  addUploadedFiles: (files: FileHandle[]) => void
  doAction: (input: string) => Promise<void>
  doCancel(): void
}

export function CopilotInputForm({machineUrl, processId, isProcessing, copilotParams, addUploadedFiles, doAction, doCancel}: CopilotInputFormProps) {
  const [input, setInput] = useState("")

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
        handleAction()
      }
    }
  }

  const handleAction = () => {
    doAction(input).then(() => {
      setInput("")
    })
  }

  return (
    <div style={{width: "100%", display: "flex", flexDirection: "row"}}>
      <div style={{display: "flex", flexDirection: "row", width: "100%"}}>
        <FileUpload machineUrl={machineUrl} process_id={processId} addUploadedFiles={addUploadedFiles}/>
        <TextField
          multiline
          variant={"standard"}
          label={copilotParams.inputLabel}
          fullWidth
          maxRows={10}
          sx={{margin: "8px 0px 8px 8px"}}
          value={input}
          onKeyDown={handleKeyDown}
          onChange={(e) => setInput(e.target.value)}
          inputProps={{"x-webkit-speech": "x-webkit-speech"}}
        />
        {copilotParams.allowSpeech && (
          <Recorder machineUrl={machineUrl} agent={copilotParams.speechAgent!} operation={copilotParams.speechOperation!} process_id={processId} setText={(text) => {
            setInput(text)
          }}/>)}
      </div>
      {isProcessing && (
        <Button variant={'text'} onClick={doCancel}><CancelRounded style={{fontSize: 36}}/></Button>
      )}
      {!isProcessing && (
        <Button
          variant={'text'}
          onClick={handleAction}><ArrowCircleUpRounded
          style={{fontSize: 36}}
          sx={{padding: "0px"}}
        /></Button>
      )}
    </div>
  )
}
