'use client'

import {ChangeEvent, useRef, useState} from "react";
import {Box, IconButton} from '@mui/material';
import AttachFileIcon from '@mui/icons-material/AttachFile';
import {uploadFile} from "../client-api-helpers/files-helper";

interface FileUploadProps {
  machineUrl: string;
  process_id: string;
}

export function FileUpload({machineUrl, process_id}: FileUploadProps) {
  const [selectedFile, setSelectedFile] = useState<Blob[]>([]);
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const handleButtonClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = async (event: ChangeEvent<HTMLInputElement>) => {
    if (event?.target?.files) {
      const blobs: Blob[] = [];
      for (let i = 0; i < event.target.files.length; i++) {
        blobs.push(event.target.files[i] as Blob)
      }
      for (const blob of blobs) {
        await uploadFile(machineUrl, process_id, blob)
      }
      setSelectedFile(blobs)
    }
  };
  // eslint-disable-next-line no-unused-vars
  const handleFileUpload = async () => {
    for (const blob of selectedFile) {
      await uploadFile(machineUrl, process_id, blob)
    }
  }

  return (
    <Box
      display={"flex"}
    >
      <input
        accept="image/*, audio/*, application/pdf, application/msword,
        application/vnd.openxmlformats-officedocument.wordprocessingml.document text/* aplication/json"
        style={{display: 'none'}}
        ref={fileInputRef}
        type="file"
        onChange={handleFileChange}
      />
      <IconButton
        onClick={handleButtonClick}
        sx={{padding: "0", justifySelf: "center", minWidth: "12px", marginTop: "8px"}}
      >
        <AttachFileIcon style={{fontSize: 28}}/>
      </IconButton>
    </Box>

  )
}
