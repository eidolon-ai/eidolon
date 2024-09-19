'use client'

import { useState } from "react";
import { AgentInputForm } from "./agent-input-form.js";
import { OperationInfo, ProcessStatus } from "@eidolon-ai/client";
import { ArrowUpCircleIcon, XCircleIcon, PlusCircleIcon, MinusCircleIcon } from 'lucide-react';
import { ButtonScrollToBottom } from "./button-scroll-to-bottom.js";

interface AgentProcessProps {
  operations: OperationInfo[]
  processState?: ProcessStatus
  handleAction: (machine: string, agent: string, operation: string, data: any) => void
  handleCancel: () => void
}

export function AgentProcess({ operations, processState, handleAction, handleCancel }: AgentProcessProps) {
  const [bigForm, setBigForm] = useState(false);

  const handleSubmit = (formJson: Record<string, any>) => {
    const operation = formJson.operation as OperationInfo;
    handleAction(operation.machine, operation.agent, operation.name, formJson.data);
  };

  const toggleFormSize = () => {
    setBigForm(!bigForm);
  };

  let content = (
    <AgentInputForm handleSubmit={handleSubmit} operations={operations} isProgram={false} processState={processState} />
  );

  let button: JSX.Element | null = (
    <button form="agent-input-form" type="submit" className="text-blue-500 hover:text-blue-700 focus:outline-none">
      <ArrowUpCircleIcon className="w-9 h-9" />
    </button>
  );

  if (processState?.state === "processing") {
    content = (
      <div className="flex flex-col items-center">
        <h2 className="text-xl font-semibold">Running...</h2>
      </div>
    );
    button = (
      <button onClick={handleCancel} className="text-red-500 hover:text-red-700 focus:outline-none">
        <XCircleIcon className="w-9 h-9" />
      </button>
    );
  } else if (!processState) {
    content = (
      <div className="space-y-4">
        <div className="h-15 bg-gray-200 animate-pulse rounded"></div>
        <div className="h-15 bg-gray-200 animate-pulse rounded"></div>
      </div>
    );
    button = <div className="w-9 h-9 bg-gray-200 animate-pulse rounded-full"></div>;
  } else if ((processState?.state === 'http_error' || processState?.state === 'error' || processState?.state === 'unhandled_error') && processState?.available_actions?.length === 0) {
    content = (
      <div className="flex flex-col items-center text-center">
        <h2 className="text-xl font-semibold text-red-600">Error</h2>
        <p className="text-gray-700">The process has encountered an error and can no longer accept input.</p>
        <p className="text-red-500">Error: {processState?.error}</p>
      </div>
    );
    button = null;
  } else if (processState?.available_actions?.length === 0) {
    content = (
      <div className="flex flex-col items-center text-center">
        <h3 className="text-lg font-semibold">Terminated</h3>
        <p className="text-gray-700">The process has terminated and can no longer accept input.</p>
      </div>
    );
    button = null;
  }

  return (
    <div className={`bg-white rounded-lg shadow-lg p-4 mb-4 transition-all duration-300 ease-in-out ${bigForm ? 'h-[70vh]' : 'h-64'} w-full`}>
      <div className="text-center -mt-12 h-12">
        <ButtonScrollToBottom />
      </div>
      <div className="flex w-full h-full">
        <div className="flex-grow h-full">
          {content}
        </div>
        <div className="flex flex-col justify-between ml-2">
          <button onClick={toggleFormSize} className="text-gray-500 hover:text-gray-700 focus:outline-none">
            {bigForm ? <MinusCircleIcon className="w-5 h-5" /> : <PlusCircleIcon className="w-5 h-5" />}
          </button>
          {button}
        </div>
      </div>
    </div>
  );
}
