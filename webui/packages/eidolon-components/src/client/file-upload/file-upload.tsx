'use client'

import { ChangeEvent, useRef, useState } from "react";
import { PaperclipIcon } from 'lucide-react';
import { setMetadata, uploadFile } from "../client-api-helpers/files-helper.ts";
import { FileHandle } from "@eidolon-ai/client";

interface CircularProgressProps {
  value: number;
}

function CircularProgressWithLabel({ value }: CircularProgressProps) {
  return (
    <div className="relative inline-flex">
      <svg className="w-8 h-8" viewBox="0 0 36 36">
        <circle
          className="stroke-gray-200"
          strokeWidth="3"
          fill="transparent"
          r="16"
          cx="18"
          cy="18"
        />
        <circle
          className="stroke-blue-600"
          strokeWidth="3"
          strokeDasharray={100}
          strokeDashoffset={100 - value}
          strokeLinecap="round"
          fill="transparent"
          r="16"
          cx="18"
          cy="18"
        />
      </svg>
      <div className="absolute inset-0 flex items-center justify-center">
        <span className="text-xs text-gray-600">{`${Math.round(value)}%`}</span>
      </div>
    </div>
  );
}

interface FileUploadProps {
  machineUrl: string;
  process_id: string;
  addUploadedFiles: (files: FileHandle[]) => void;
}

export function FileUpload({ machineUrl, process_id, addUploadedFiles }: FileUploadProps) {
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const [uploadingFiles, setUploadingFiles] = useState(false);
  const [progress, setProgress] = useState(0);

  const handleButtonClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = async (event: ChangeEvent<HTMLInputElement>) => {
    if (event?.target?.files) {
      const blobs = Array.from(event.target.files);

      setUploadingFiles(true);
      setProgress(0);
      try {
        const fileHandles: FileHandle[] = [];
        for (const blob of blobs) {
          const fileHandle = await uploadFile(machineUrl, process_id, blob);
          if (fileHandle) {
            await setMetadata(machineUrl, process_id, fileHandle.fileId, { name: blob.name });
            fileHandles.push(fileHandle);
          }
          setProgress((fileHandles.length / blobs.length) * 100);
        }
        addUploadedFiles(fileHandles);
      } finally {
        setProgress(0);
        setUploadingFiles(false);
      }
    }
  };

  return (
    <div className="flex items-center">
      <input
        className="hidden"
        accept="image/*, audio/*, application/pdf, application/msword, application/vnd.openxmlformats-officedocument.wordprocessingml.document, text/*, application/json"
        multiple
        ref={fileInputRef}
        type="file"
        onChange={handleFileChange}
      />
      {uploadingFiles ? (
        <div className="w-8 h-8 flex items-center justify-center">
          <CircularProgressWithLabel value={progress} />
        </div>
      ) : (
        <button
          onClick={handleButtonClick}
          className="p-1 rounded-full hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <PaperclipIcon className="w-6 h-6 text-gray-600" />
        </button>
      )}
    </div>
  );
}