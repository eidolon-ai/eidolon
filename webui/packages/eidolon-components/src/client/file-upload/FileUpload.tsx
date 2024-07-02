'use client'

import {ChangeEvent, useRef, useState} from "react";
import {Box, CircularProgress, CircularProgressProps, IconButton, Typography} from '@mui/material';
import AttachFileIcon from '@mui/icons-material/AttachFile.js';
import {setMetadata, uploadFile} from "../client-api-helpers/files-helper.ts";
import {FileHandle} from "@eidolon/client";

function CircularProgressWithLabel(
  props: CircularProgressProps & { value: number },
) {
  return (
    <Box sx={{position: 'relative', display: 'inline-flex'}}>
      <CircularProgress variant="determinate" {...props}/>
      <Box
        sx={{
          top: 0,
          left: 0,
          bottom: 0,
          right: 0,
          position: 'absolute',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        <Typography
          variant="caption"
          component="div"
          color="text.secondary"
        >{`${Math.round(props.value)}%`}</Typography>
      </Box>
    </Box>
  );
}

interface FileUploadProps {
  machineUrl: string;
  process_id: string;
  // eslint-disable-next-line no-unused-vars
  addUploadedFiles: (files: FileHandle[]) => void;
}

export function FileUpload({machineUrl, process_id, addUploadedFiles}: FileUploadProps) {
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const [uploadingFiles, setUploadingFiles] = useState(false);
  const [progress, setProgress] = useState(0);

  const handleButtonClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = async (event: ChangeEvent<HTMLInputElement>) => {
    if (event?.target?.files) {
      const blobs: File[] = [];
      for (let i = 0; i < event.target.files.length; i++) {
        blobs.push(event.target.files[i] as File)
      }

      setUploadingFiles(true)
      setProgress(0)
      try {
        const fileHandles: FileHandle[] = []
        for (const blob of blobs) {
          let fileHandle = (await uploadFile(machineUrl, process_id, blob))!
          await setMetadata(machineUrl, process_id, fileHandle.fileId, {name: blob.name})
          fileHandles.push(fileHandle!)
          setProgress((fileHandles.length / blobs.length) * 100)
        }
        addUploadedFiles(fileHandles)
      } finally {
        setProgress(0)
        setUploadingFiles(false)
      }

    }
  };

  return (
    <Box
      display={"flex"}
    >
      <input
        accept="image/*, audio/*, application/pdf, application/msword,
        application/vnd.openxmlformats-officedocument.wordprocessingml.document text/* aplication/json"
        style={{display: 'none'}}
        multiple
        ref={fileInputRef}
        type="file"
        onChange={handleFileChange}
      />
      {uploadingFiles && (
        <IconButton
          disabled={true}
          sx={{padding: "0", justifySelf: "center", width: "28px", minWidth: "12px", marginTop: "8px"}}
        >
          <CircularProgressWithLabel value={progress}/>
        </IconButton>
      )}
      {!uploadingFiles && (
        <IconButton
          onClick={handleButtonClick}
          sx={{padding: "0", justifySelf: "center", minWidth: "12px", marginTop: "8px"}}
        >
          <AttachFileIcon style={{fontSize: 28}}/>
        </IconButton>
      )}
    </Box>
  )
}
