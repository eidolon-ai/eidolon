'use client'

import {usePathname, useRouter} from "next/navigation";
import {PlusCircle} from "lucide-react";
import {CopilotParams, createProcess, EidolonApp, ProcessList, useProcesses} from "@eidolon-ai/components/client";
import {ProcessStatus} from "@eidolon-ai/client";

export interface ProcessListPanelProps {
  app: EidolonApp
}

export function ProcessListPanel({ app }: ProcessListPanelProps) {
  const machineURL = app.location;
  const {updateProcesses} = useProcesses();
  const router = useRouter();
  const pathname = usePathname();

  const addClicked = () => {
    if (app.type === 'copilot') {
      const options = app.params as CopilotParams;
      createProcess(machineURL, options.agent, options.newItemText || "New Chat").then((process: ProcessStatus | null) => {
        if (process) {
          router.push(`/eidolon-apps/${app.path}/${process.process_id}`);
        }
      }).then(() => updateProcesses(machineURL));
    } else {
      router.push(`/eidolon-apps/${app.path}`);
    }
  };

  return (
    <div className="overflow-auto h-full">
      <div className="h-full">
        <ul className="list-none p-0 m-0">
          <li className="p-0">
            <button
              onClick={addClicked}
              className="flex items-center w-full px-4 py-2 hover:bg-gray-100 transition-colors duration-200"
            >
              <PlusCircle className="w-6 h-6 mr-4 text-gray-600"/>
              <span className="text-sm">{app.params.addBtnText || "New Conversation"}</span>
            </button>
          </li>
        </ul>

        <hr className="my-2 border-t border-gray-200"/>

        <ProcessList
          machineURL={machineURL}
          isSelected={(process: ProcessStatus) => pathname.includes(process.process_id)}
          selectChat={(process: ProcessStatus) => {
            router.push(`/eidolon-apps/${app.path}/${process.process_id}`);
          }}
          goHome={() => {
          }}
        />
      </div>
    </div>
  );
}