import { useState, KeyboardEvent, ChangeEvent } from 'react';
import { ArrowUpCircleIcon, XCircleIcon } from 'lucide-react';
import { CopilotParams } from '../lib/util.ts';
import { FileUpload } from '../file-upload/file-upload.tsx';
import { FileHandle } from '@eidolon-ai/client';
import { CircularProgressWithContent } from '../lib/circular-progress-with-content.tsx';
import RecorderElement from '../audio/recorder-element.js';

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

export function ProcessError({ error }: { error: string }) {
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
      <div className="w-10 h-10 bg-gray-200 animate-pulse rounded-full"></div>
    </div>
  );
}

interface CopilotInputFormProps {
  machineUrl: string;
  processId: string;
  isProcessing: boolean;
  copilotParams: CopilotParams;
  addUploadedFiles: (files: FileHandle[]) => void;
  doAction: (input: string) => Promise<void>;
  doCancel: () => void;
}

export function CopilotInputForm({
  machineUrl,
  processId,
  isProcessing,
  copilotParams,
  addUploadedFiles,
  doAction,
  doCancel
}: CopilotInputFormProps) {
  const [input, setInput] = useState('');

  const handleKeyDown = async (event: KeyboardEvent<HTMLTextAreaElement>) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      await handleAction();
    }
  };

  const handleAction = async () => {
    setInput('');
    await doAction(input);
  };

  return (
    <div className="w-full flex flex-row">
      <div className="flex flex-row w-full">
        <FileUpload
          machineUrl={machineUrl}
          process_id={processId}
          addUploadedFiles={addUploadedFiles}
        />
        <div className="flex-grow mx-2">
          <textarea
            className="w-full mt-2 p-1 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none max-h-[240px]"
            style={{overflow: 'auto'}}
            placeholder={copilotParams.inputLabel}
            value={input}
            onChange={(e: ChangeEvent<HTMLTextAreaElement>) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
          />
        </div>
        {copilotParams.allowSpeech && (
          <RecorderElement
            machineUrl={machineUrl}
            agent={copilotParams.speechAgent!}
            operation={copilotParams.speechOperation!}
            setText={(text: string) => {
              setInput(text);
              handleAction();
            }}
          />
        )}
      </div>
      {isProcessing ? (
        <div className="flex items-center">
        <CircularProgressWithContent>
            <button
              onClick={doCancel}
              className="text-red-500 hover:text-red-700 focus:outline-none"
            >
              <XCircleIcon className="w-8 h-8" />
            </button>
          </CircularProgressWithContent>
        </div>
      ) : (
        <button
          onClick={handleAction}
          className="ml-2 text-blue-500 hover:text-blue-700 focus:outline-none"
        >
          <ArrowUpCircleIcon className="w-8 h-8" />
        </button>
      )}
    </div>
  );
}