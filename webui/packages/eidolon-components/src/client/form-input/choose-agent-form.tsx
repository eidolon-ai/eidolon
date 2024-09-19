'use client'

import { useEffect, useState } from "react";
import { createProcess } from "../client-api-helpers/process-helper.ts";
import { getAgents } from "../client-api-helpers/machine-helper.ts";

export interface ChooseAgentFormProps {
  machineUrl: string,
  handleSubmit: (process_id: string) => void
  defaultAgent?: string
}

export function ChooseAgentForm({ handleSubmit, machineUrl, defaultAgent }: ChooseAgentFormProps) {
  const [title, setTitle] = useState<string>("New Conversation")
  const [agent, setAgent] = useState<string>("")
  const [agents, setAgents] = useState<string[]>([])

  const internalHandleSubmit = () => {
    if (!agent) {
      throw new Error("Agent is required")
    }
    createProcess(machineUrl, agent, title).then((process) => {
      handleSubmit(process?.process_id!)
    })
  }

  useEffect(() => {
    getAgents(machineUrl).then((agents) => {
      setAgents(agents)
      if (agents.length > 0 && !agent) {
        if (defaultAgent && agents.includes(defaultAgent)) {
          setAgent(defaultAgent)
        } else if (agents[0]) {
          setAgent(agents[0])
        }
      }
    }).catch(() => {
      // ignore
    })
  }, [machineUrl]);

  return (
    <form
      id="start-program-form"
      className="w-full"
      onSubmit={(event) => {
        event.preventDefault();
        internalHandleSubmit()
      }}
    >
      <div className="flex flex-col w-full">
        <div className="mb-4">
          <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
            Title
          </label>
          <input
            type="text"
            id="title"
            required
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
            value={title}
            onChange={(event) => setTitle(event.target.value)}
          />
        </div>
        <div className="mb-4">
          <label htmlFor="agent" className="block text-sm font-medium text-gray-700 mb-1">
            Operation
          </label>
          <select
            id="agent"
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
            value={agent}
            onChange={(event) => setAgent(event.target.value)}
          >
            {agents.map((agent, index) => (
              <option key={index} value={agent}>{agent}</option>
            ))}
          </select>
        </div>
      </div>
    </form>
  )
}