import React, { useEffect, useState } from "react";
import { createProcess, deleteProcess } from "../client-api-helpers/process-helper.ts";
import { executeOperation } from "../client-api-helpers/process-event-helper.ts";
import { uploadFile } from "../client-api-helpers/files-helper.ts";
import { Mic, MicOff, Square } from 'lucide-react';

interface RecorderProps {
  machineUrl: string;
  agent: string;
  operation: string
  // eslint-disable-next-line no-unused-vars
  setText: (text: string) => void;
}

export default function Recorder({ machineUrl, agent, operation, setText }: RecorderProps) {
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
    navigator.mediaDevices.getUserMedia({ audio: true })
      .then((stream) => {
        const mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.ondataavailable = (event) => {
          if (event.data.size > 0) {
            audioChunks.push(event.data)
            setAudioChunks(audioChunks);
          }
        };
        mediaRecorder.start();
        mediaRecorder.onstop = async () => {
          const mimeType = mediaRecorder.mimeType;
          const localChunks = audioChunks.filter((chunk) => chunk.size > 0);
          const blob = new Blob(localChunks, { type: mimeType });
          if (blob.size > 0) {
            const process = await createProcess(machineUrl, agent, "audio");
            const fileId = await uploadFile(machineUrl, process?.process_id!, blob);
            const result = await executeOperation(machineUrl, agent, operation, process?.process_id!, { audio: fileId });
            await deleteProcess(machineUrl, process?.process_id!);
            setText(result["response"]);
          }
          setAudioChunks([]);
        };
        setRecorder(mediaRecorder);
        setRecording(true);
      }).catch(err => {
        if (err.name === 'NotAllowedError') {
          setRecordingDeviceError("Microphone access denied by the user.");
          console.error('Microphone access denied by the user.');
        } else {
          setRecordingDeviceError(`Error accessing media devices: ${err}`);
          console.error('Error accessing media devices:', err);
        }
      });
  };

  const stopRecording = async () => {
    if (recorder) {
      recorder.requestData();
      recorder.stream.getTracks().forEach(track => track.stop());
      recorder.stop();
      setRecorder(null);
      setRecording(false);
    }
  };

  return (
    <>
      {recordingDeviceError && (
        <div className="group relative">
          <button className="p-2 text-gray-500 hover:text-gray-700 transition-colors duration-200">
            <MicOff size={28} />
          </button>
          <span className="absolute bottom-full left-1/2 -translate-x-1/2 bg-gray-800 text-white text-xs rounded py-1 px-2 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
            Please allow access to the microphone in your browser.
          </span>
        </div>
      )}
      {!recordingDeviceError && !recording && (
        <button
          onClick={startRecording}
          className="p-2 text-gray-500 hover:text-gray-700 transition-colors duration-200"
        >
          <Mic size={28} />
        </button>
      )}
      {!recordingDeviceError && recording && (
        <button
          onClick={stopRecording}
          className="p-2 text-red-500 hover:text-red-700 transition-colors duration-200"
        >
          <Square size={28} />
        </button>
      )}
    </>
  );
}