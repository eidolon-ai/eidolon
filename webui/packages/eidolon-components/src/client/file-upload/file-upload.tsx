'use client'

import {ChangeEvent, useRef, useState} from "react";
import {PaperclipIcon} from 'lucide-react';

interface CircularProgressProps {
  value: number;
}

function CircularProgressWithLabel({value}: CircularProgressProps) {
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

export interface SelectedFile {
  name: string
  blob: Blob
}

interface FileUploadProps {
  addUploadedFiles: (files: SelectedFile[]) => void;
}

export function FileUpload({
  addUploadedFiles,
}: FileUploadProps) {
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const [blobs, setBlobs] = useState<SelectedFile[]>([]);

  const handleButtonClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    if (event?.target?.files) {
      const newBlobs = Array.from(event.target.files).map(file => {
        return {name: file.name, blob: file};
      })
      addUploadedFiles(newBlobs);
      setBlobs([...blobs, ...newBlobs]);
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
      <div
        onClick={handleButtonClick}
        className="p-2 flex h-fit justify-center rounded-md hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <PaperclipIcon className="w-4 h-4 text-gray-600"/>
      </div>
    </div>
  );
}