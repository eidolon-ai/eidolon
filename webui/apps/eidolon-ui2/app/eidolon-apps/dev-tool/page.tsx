'use client'

import {EidolonApp, getApp, getAgents, getOperations, createProcess} from "@eidolon-ai/components/client";
import {OperationInfo, ProcessStatus} from "@eidolon-ai/client";
import {ChevronDown, ChevronRight, Code} from 'lucide-react';
import {useEffect, useState} from 'react';
import {useRouter} from "next/navigation";

interface AgentOperations {
  [agent: string]: OperationInfo[];
}

const DevTools: React.FC = () => {
  const [app, setApp] = useState<EidolonApp | undefined>(undefined);
  const [expandedAgents, setExpandedAgents] = useState<Record<string, boolean>>({});
  const router = useRouter();

  useEffect(() => {
    getApp('dev-tool').then(async (app: EidolonApp) => {
      const agentNames: string[] = await getAgents(app.location);
      const agents: AgentOperations = {};
      await Promise.all(agentNames.sort().map(async (agent) => {
        agents[agent] = await getOperations(app.location, agent);
      }));

      app.agents = agents;
      setApp(app);
      setExpandedAgents(Object.fromEntries(agentNames.map(agent => [agent, false])));
    });
  }, []);

  const toggleAgent = (agent: string) => {
    setExpandedAgents(prev => ({...prev, [agent]: !prev[agent]}));
  };

  function executeOperation(agent: string, operation: string) {
    createProcess(app!.location, agent, `${agent}:${operation}`).then((process: ProcessStatus) => {
      router.push(`/eidolon-apps/dev-tool/${process.process_id}/${operation}`);
    })
  }

  return (
    <main className="flex-grow p-6 flex flex-col items-center justify-center h-full bg-gray-100">
      <div className="w-[65vw] h-full bg-white rounded-lg shadow-md overflow-hidden max-w-full flex flex-col">
        {app && (
          <>
            <div className="bg-gradient-to-b from-gray-600 to-gray-400 p-4">
              <h2 className="text-2xl font-bold text-white">{app.name}</h2>
            </div>
            <div className="flex-grow overflow-y-auto">
              <div className="p-4">
                <p className="text-sm text-gray-600 mb-4">{app.description}</p>
                {app.agents && Object.keys(app.agents).sort().map(agent => (
                  <div key={agent} className="mb-4">
                    <button
                      onClick={() => toggleAgent(agent)}
                      className="flex items-center justify-between w-full p-2 bg-gray-100 hover:bg-gray-200 rounded-md transition-colors duration-200"
                    >
                      <span className="text-lg font-semibold">{agent}</span>
                      {expandedAgents[agent] ? <ChevronDown size={20}/> : <ChevronRight size={20}/>}
                    </button>
                    {expandedAgents[agent] && (
                      <ul className="list-none mt-2 space-y-2">
                        {(app.agents[agent] as OperationInfo[]).map(operation => (
                          <li key={operation.name} className="bg-white p-3 rounded-md shadow-sm group">
                            <div className={"flex justify-between items-center"}>
                              <div className="flex items-center space-x-2 mb-1">
                                <Code size={16} className="text-blue-500"/>
                                <span className="font-medium">{operation.summary} ({operation.name})</span>
                              </div>
                              <button className="text-blue-400 underline opacity-0 group-hover:opacity-100 transition-opacity duration-200" onClick={() => executeOperation(agent, operation.name)}>Execute</button>
                            </div>
                            {operation.description && (
                              <div className="mt-2 flex items-start space-x-2 ml-6">
                                <p className="text-sm text-gray-600">{operation.description}</p>
                              </div>
                            )}
                            {operation.schema.properties && (
                              <div className="mt-2 flex flex-col items-start space-x-2 ml-6">
                                <p className="text-sm text-gray-600">Parameters:</p>
                                <table>
                                  <tbody>
                                  {Object.entries(operation.schema.properties).map(([name, in_prop]) => {
                                    const prop = in_prop as any;
                                    return (
                                      <tr key={name} className="text-gray-700">
                                        <td>
                                          <div className={"mr-2 w-full font-semibold"}>{name}:</div>
                                        </td>
                                        <td><span className={"italic"}>{prop.type}</span></td>
                                        <td><span className="ml-2 text-sm text-gray-600">{prop.description}</span></td>
                                      </tr>
                                    )
                                  })}
                                  </tbody>
                                </table>
                              </div>
                            )}
                          </li>
                        ))}
                      </ul>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </>
        )}
      </div>
    </main>
  );
}

export default DevTools;