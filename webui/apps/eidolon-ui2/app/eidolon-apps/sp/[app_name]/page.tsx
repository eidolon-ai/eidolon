'use client'

import React, {useEffect, useState} from 'react';
import {CopilotInputForm, CopilotParams, createProcess, getOperations, SelectedFile, useApp} from "@eidolon-ai/components/client";
import {ArrowRight, MessageSquare} from 'lucide-react';
import {useNewChatOptions} from "./new-chat-options.tsx";
import {useRouter} from "next/navigation";
import {OperationInfo, ProcessStatus} from "@eidolon-ai/client"

export interface HomePageProps {
  params: {
    app_name: string
  }
}

const ChatbotHomePage = ({params}: HomePageProps) => {
  const [supportedLLMs, setSupportedLLMs] = useState<string[] | undefined>()
  const [selectedLLM, setSelectedLLM] = useState<string | undefined>()
  const {app} = useApp()
  const {setOptions} = useNewChatOptions()
  const router = useRouter()
  const copilotParams = app?.params as CopilotParams;

  useEffect(() => {
    if (app) {
      getOperations(app.location, copilotParams.agent).then((operations: OperationInfo[]) => {
        const operation = operations.find((o) => o.name === copilotParams.operation)
        if (operation) {
          copilotParams.operationInfo = operation
          if (operation.schema?.properties?.execute_on_apu) {
            const property = operation.schema?.properties?.execute_on_apu as Record<string, any>
            setSupportedLLMs(property?.["enum"] as string[])
            setSelectedLLM(property?.default as string)
          }
        }
      })
    }
  }, [app])

  const doAction = async (input: string, files: SelectedFile[], selectedLLM: string) => {
    createProcess(app.location, app.params.agent, "").then((process: ProcessStatus) => {
      setOptions({
        input: input,
        files: files,
        selectedLLM: selectedLLM,
        operation: copilotParams.operation
      })
      router.push(`/eidolon-apps/sp/${params.app_name}/${process.process_id}`)
    })
  };


  return (
    <main className="flex-grow p-6 flex flex-col items-center justify-center h-full bg-gray-100">
      <div className="w-[65vw] h-full max-w-full flex flex-col">
        {app && (
          <div className="flex flex-col items-center w-full h-full font-serif gap-2">
            <div className={"p-2 m-2 w-full rounded-lg border-gray-200 border-solid bg-white shadow-md overflow-hidden "}>
              <CopilotInputForm
                inputLabel={copilotParams.inputLabel}
                selectedLLM={selectedLLM}
                setSelectedLLM={setSelectedLLM}
                supportedLLMs={supportedLLMs}
                speechOptions={copilotParams?.speechAgent && copilotParams?.speechOperation ? {
                  machineUrl: app?.location,
                  agent: copilotParams?.speechAgent,
                  operation: copilotParams?.speechOperation,
                } : undefined}
                doAction={doAction}
                handleCancel={() => {}}
                processState={"idle"}
              />
            </div>
            <div className="flex-grow container mx-auto bg-white rounded-lg shadow-md overflow-hidden">

              <div className="p-6 space-y-6">
                <h2 className="text-2xl font-semibold text-gray-800">{app.name}</h2>

                <div className="space-y-4">
                  <p className="text-gray-600">
                    {app.description}
                  </p>
                </div>

                <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded-md">
                  <div className="flex items-center space-x-3">
                    <MessageSquare className="h-6 w-6 text-blue-500"/>
                    <p className="text-blue-700 font-medium">Start a conversation</p>
                  </div>
                  <p className="mt-2 text-blue-600">
                    Type your message in the box above and hit enter to start chatting with Eidolon.
                    You can also upload files or use voice input if available.
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </main>
  );
};

export default ChatbotHomePage;
