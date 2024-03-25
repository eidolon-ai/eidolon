import {useEffect, useState} from "react";
import {createProcess} from "../client-api-helpers/process-helper";
import {executeOperation} from "../client-api-helpers/process-event-helper";
import {Button, Tooltip} from "@mui/material";
import StopIcon from '@mui/icons-material/Stop';
import {uploadFile} from "../client-api-helpers/files-helper";
import MicIcon from '@mui/icons-material/Mic';
import MicOffIcon from '@mui/icons-material/MicOff';

interface RecorderProps {
  machineUrl: string;
  agent: string;
  process_id: string;
  operation: string
  // eslint-disable-next-line no-unused-vars
  setText: (text: string) => void;
}

export default function Recorder({machineUrl, agent, process_id, operation, setText}: RecorderProps) {
  const [recording, setRecording] = useState(false);
  const [recordingDeviceError, setRecordingDeviceError] = useState<string | null>(null);
  const [recorder, setRecorder] = useState<MediaRecorder | null>(null);
  const [audioChunks, setAudioChunks] = useState<Blob[]>([]);

  useEffect(() => {
    if (!(navigator.mediaDevices && window.MediaRecorder)) {
      console.error("getUserMedia not supported on your browser!");
      setRecordingDeviceError("getUserMedia not supported on your browser.");
    }
  }, []);

  const startRecording = () => {
    navigator.mediaDevices.getUserMedia(
      // constraints - only audio needed for this app
      {
        audio: true,
      },
    )
      // Success callback
      .then((stream) => {
        const mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.ondataavailable = (event) => {
          if (event.data.size > 0) {
            audioChunks.push(event.data)
            setAudioChunks(audioChunks);
          }
        };
        mediaRecorder.start()
        mediaRecorder.onstop = async () => {
          const mimeType = mediaRecorder.mimeType;
          const localChunks = audioChunks.filter((chunk) => chunk.size > 0);
          const blob = new Blob(localChunks, {type: mimeType});
          if (blob.size > 0) {
            const process = await createProcess(machineUrl, agent, "audio");
            const fileId = await uploadFile(machineUrl, process?.process_id!, blob);
            const result = await executeOperation(machineUrl, agent, operation, process?.process_id!, {audio: {machineURL: machineUrl, process_id: process_id, file_id: fileId}});
            setText(result["response"])
          }
          setAudioChunks([]);
        }
        setRecorder(mediaRecorder);
        setRecording(true);
      }).catch(err => {
      if (err.name === 'NotAllowedError') {
        setRecordingDeviceError("Microphone access denied by the user.");
        console.error('Microphone access denied by the user.');
        // Handle the case when the user denies microphone access
      } else {
        setRecordingDeviceError(`Error accessing media devices:${err}`);
        console.error('Error accessing media devices:', err);
      }
    })
  }

  const stopRecording = async () => {
    if (recorder) {
      recorder.requestData()
      for (const track of recorder.stream.getTracks()) {
        track.stop();
      }
      recorder.stop();
      setRecorder(null);
      setRecording(false);

    }
  }

  return (
    <>
      {recordingDeviceError && (
        <Tooltip title={"Please allow access to the microphone in your browser."}>
          <Button color={"secondary"} sx={{padding: "0", minWidth:"12px", marginTop: "8px"}} variant={'text'}><MicOffIcon style={{fontSize: 28}}/></Button>
        </Tooltip>
      )}
      {!recordingDeviceError && !recording && (<Button color={"secondary"} sx={{padding: "0", minWidth:"12px", marginTop: "8px"}} variant={'text'} onClick={startRecording}><MicIcon style={{fontSize: 28}}/></Button>)}
      {!recordingDeviceError && recording && (<Button color={"secondary"} sx={{padding: "0", minWidth:"12px", marginTop: "8px"}} variant={'text'} onClick={stopRecording}><StopIcon style={{fontSize: 28}}/></Button>)}
    </>
  )
}
