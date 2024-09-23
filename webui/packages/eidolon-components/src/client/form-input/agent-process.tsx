'use client'

import {useEffect, useState} from "react";
import {AgentInputForm} from "./agent-input-form.js";
import {OperationInfo} from "@eidolon-ai/client";
import {AlertCircle, ArrowUpCircleIcon, CheckCircle2, Loader2, MinusCircleIcon, PlusCircleIcon, RefreshCw, XCircleIcon} from 'lucide-react';
import {ButtonScrollToBottom} from "./button-scroll-to-bottom.js";
import {getOperations} from "../client-api-helpers/machine-helper.js";
import {useApp} from "../hooks/app-context.js";
import {useProcess} from "../hooks/process_context.js";

interface AgentProcessProps {
  selectedOperation?: string
  handleAction: (operation: string, data: any) => Promise<void>
  handleCancel: () => void
  handleNewConversation: () => void
}

export function AgentProcess({ selectedOperation, handleAction, handleCancel, handleNewConversation }: AgentProcessProps) {
  const [bigForm, setBigForm] = useState(false);
  const [formData, setFormData] = useState<any>({});
  const [agentOperation, setAgentOperation] = useState<string | undefined>(selectedOperation);
  const [operations, setOperations] = useState<OperationInfo[]>([]);
  const {app} = useApp()
  const {processStatus: processState} = useProcess()

  useEffect(() => {
    if (app && processState) {
      getOperations(app?.location, processState.agent).then(operations => {
        setOperations(operations);
        if (!agentOperation) {
          setAgentOperation(operations[0]?.name);
        }
      })
    }
  }, [app, processState])

  const handleSubmit = async (formJson: Record<string, any>) => {
    const operation = operations.find(op => op.name === agentOperation)!;
    console.log("submitting", operation.machine, operation.agent, operation.name, formJson);
    await handleAction(operation.name, formJson);
  };

  const toggleFormSize = () => {
    setBigForm(!bigForm);
  };

  const renderStateContent = () => {
    if (!processState) {
      return (
        <div className="flex flex-col items-center justify-center h-full">
          <Loader2 className="h-8 w-8 animate-spin text-blue-500 mb-2" />
          <h2 className="text-lg font-semibold">Loading</h2>
          <p className="text-gray-600">Please wait while we process your request...</p>
        </div>
      );
    }

    if (processState.state === "processing") {
      return (
        <div className="flex flex-col items-center justify-center h-full">
          <Loader2 className="h-8 w-8 animate-spin text-blue-500 mb-2" />
          <h2 className="text-lg font-semibold">Running...</h2>
          <p className="text-gray-600">Your request is being processed.</p>
        </div>
      );
    }

    if (processState.state === 'http_error' || processState.state === 'error' || processState.state === 'unhandled_error') {
      return (
        <div className="flex flex-col items-center justify-center h-full">
          <AlertCircle className="h-8 w-8 text-red-500 mb-2" />
          <h2 className="text-lg font-semibold text-red-600">Error</h2>
          <p className="text-gray-600 text-center">An error occurred. Please try starting a new conversation.</p>
          <p className="text-red-500 mt-2">{processState.error}</p>
          <button
            onClick={handleNewConversation}
            className="mt-4 flex items-center space-x-2 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition-colors"
          >
            <RefreshCw className="h-4 w-4" />
            <span>New Conversation</span>
          </button>
        </div>
      );
    }

    if (processState.available_actions?.length === 0) {
      return (
        <div className="flex flex-col items-center justify-center h-full">
          <CheckCircle2 className="h-8 w-8 text-green-500 mb-2" />
          <h2 className="text-lg font-semibold">Conversation Terminated</h2>
          <p className="text-gray-600 text-center">This conversation has ended. You can start a new one.</p>
          <button
            onClick={handleNewConversation}
            className="mt-4 flex items-center space-x-2 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition-colors"
          >
            <RefreshCw className="h-4 w-4" />
            <span>New Conversation</span>
          </button>
        </div>
      );
    }

    return (
      <AgentInputForm
        formData={formData}
        setFormData={setFormData}
        agentOperation={agentOperation}
        setAgentOperation={setAgentOperation}
        operations={operations}
        onSubmit={() => {handleSubmit(formData)}}
      />
    );
  };

  const renderActionButton = () => {
    if (!processState || processState.state === "processing") {
      return (
        <button onClick={handleCancel} className="text-red-500 hover:text-red-700 focus:outline-none">
          <XCircleIcon className="w-9 h-9" />
        </button>
      );
    }

    if (processState.state === 'http_error' || processState.state === 'error' || processState.state === 'unhandled_error' || processState.available_actions?.length === 0) {
      return null;
    }

    return (
      <button form="agent-input-form" onClick={() => handleSubmit(formData)} className="text-blue-500 hover:text-blue-700 focus:outline-none">
        <ArrowUpCircleIcon className="w-9 h-9" />
      </button>
    );
  };

  return (
    <div className={`font-sans bg-white rounded-lg shadow-lg p-4 mb-4 transition-all duration-300 ease-in-out ${bigForm ? 'h-[70vh]' : 'h-64'} w-full`}>
      <div className="text-center -mt-12 h-12">
        <ButtonScrollToBottom />
      </div>
      <div className="flex w-full h-full">
        <div className="flex-grow h-full">
          {renderStateContent()}
        </div>
        <div className="flex flex-col justify-between ml-2">
          <button onClick={toggleFormSize} className="text-gray-500 hover:text-gray-700 focus:outline-none">
            {bigForm ? <MinusCircleIcon className="w-5 h-5" /> : <PlusCircleIcon className="w-5 h-5" />}
          </button>
          {renderActionButton()}
        </div>
      </div>
    </div>
  );
}