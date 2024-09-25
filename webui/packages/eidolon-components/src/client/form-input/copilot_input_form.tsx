'use client'

import React, {useState} from 'react';
import RecorderElement, {SpeechOptions} from '../audio/recorder-element.js';
import CustomTextarea from "./custom_text_area.js";
import {ArrowUp, FileText, XCircleIcon} from "lucide-react";
import {CircularProgressWithContent} from "../lib/circular-progress-with-content.js";
import {FileUpload, SelectedFile} from "../file-upload/file-upload.js";
import StyledSelect from "./styled-select.js";

export function ProcessTerminated() {
  return (
    <div className="w-full flex flex-col items-center text-center">
      <h3 className="text-xl font-semibold mb-2">Terminated</h3>
      <p className="text-gray-600">
        The process has terminated and can no longer accept input.
      </p>
    </div>
  );
}

export function ProcessError({error}: { error: string }) {
  return (
    <div className="w-full flex flex-col items-center text-center">
      <h2 className="text-2xl font-bold text-red-600 mb-2">Error</h2>
      <p className="text-gray-700 mb-2">
        The process has encountered an error and can no longer accept input.
      </p>
      <p className="text-red-500">
        Error: {error}
      </p>
    </div>
  );
}

export function ProcessLoading() {
  return (
    <div className="w-full flex items-center space-x-4">
      <div className="flex-grow h-16 bg-gray-200 animate-pulse rounded"></div>
    </div>
  );
}

interface CopilotInputFormProps {
  inputLabel: string
  processState: string,
  supportedLLMs: string[] | undefined,
  selectedLLM?: string,
  setSelectedLLM: (llm: string) => void,
  speechOptions?: SpeechOptions,
  doAction: (input: string, files: SelectedFile[], selectedLLM?: string) => Promise<void>;
  handleCancel: () => void
}

export function CopilotInputForm({
                                   inputLabel,
                                   processState,
                                   supportedLLMs,
                                   selectedLLM,
                                   setSelectedLLM,
                                   speechOptions,
                                   doAction,
                                   handleCancel,
                                 }: CopilotInputFormProps) {
  const [uploadedFiles, setUploadedFiles] = useState<SelectedFile[]>([]);
  const [input, setInput] = useState('');

  const addUploadedFiles = (files: SelectedFile[]) => {
    setUploadedFiles([...uploadedFiles, ...files]);
  }

  const removeFile = (index: number) => {
    setUploadedFiles(uploadedFiles.filter((_, i) => i !== index));
  }

  const handleAction = () => {
    const inputText = input.trim()
    setInput('')
    doAction(inputText, uploadedFiles, selectedLLM).then()
  }

  return (
    <div className="font-sans w-full flex flex-col bg-white">
      {uploadedFiles && uploadedFiles.length > 0 && (
        <div className="flex flex-row items-center justify-start p-2 border-t-0 border-x-0 border-b border-dashed border-gray-200">
          <div className="flex items-center justify-center text-gray-400 gap-2">
            {uploadedFiles.map((file, i) => {
              return (
                <div className="flex flex-row items-center text-xs font-light hover:bg-gray-200 p-1" key={i}>
                  <FileText className="h-4 w-4"/>
                  <span className="mr-1">{file?.name}</span>
                  <XCircleIcon onClick={() => removeFile(i)} className="w-4 h-4 text-red-500"/>
                </div>
              )
            })}
          </div>
        </div>
      )}

      <div className={"p-2"}>
        <div className="w-full flex flex-row pr-2">
          <div className="w-full flex flex-row justify-center items-center">
            {speechOptions && (
              <RecorderElement
                speechOptions={speechOptions}
                setText={(text: string) => {
                  if (text.trim().length > 0) {
                    doAction(text.trim(), uploadedFiles, selectedLLM).then()
                  }
                }}
              />
            )}
            <div
              id={"chat-input"}
              className="flex flex-row w-full">
              <div className="flex-grow mr-2">
                <CustomTextarea
                  placeholder={inputLabel}
                  ariaLabel={inputLabel}
                  value={input}
                  onChange={setInput}
                  handleEnter={handleAction}
                />
              </div>
            </div>
          </div>
          <div className={"flex flex-row justify-center items-start"}>
            <div className={"flex flex-row justify-center items-center gap-2"}>
              {processState === "processing" ? (
                <div className="flex items-center">
                  <CircularProgressWithContent>
                    <button
                      onClick={handleCancel}
                      className="p-1 text-red-500 hover:text-red-700 focus:outline-none"
                    >
                      <XCircleIcon className="w-4 h-4"/>
                    </button>
                  </CircularProgressWithContent>
                </div>
              ) : (
                <button
                  id={'submit-chat'}
                  onClick={handleAction}
                  className={`p-1 text-white bg-[#FF6341bb] hover:bg-[#FF6341ff] focus:outline-none justify-center items-center rounded-md flex ${input && input.length > 0 ? "visible" : "invisible"}`}
                >
                  <ArrowUp className="w-4 h-4"/>
                </button>
              )}
              <div className={"flex flex-row justify-center"}>
                <FileUpload addUploadedFiles={addUploadedFiles}/>
              </div>
            </div>
          </div>
        </div>
        <div className="flex flex-row justify-between mx-2">
          {supportedLLMs && (
            <StyledSelect
              options={supportedLLMs}
              value={selectedLLM || supportedLLMs[0] || ''}
              onChange={setSelectedLLM}
              size="sm"
            />
          )}
          <p className={`text-xs self-end mb-1.5 text-gray-400 ${input && input.length ? 'opacity-100' : 'opacity-0'}`}>
            Press <span className={"bg-blue-50 p-1"}>Shift-Enter</span> to add a line
          </p>
        </div>
      </div>
    </div>
  )
}