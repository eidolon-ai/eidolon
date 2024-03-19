import {notFound} from "next/navigation";
import {_processHandler} from "../../../api/eidolon/eidolon_helpers";
import manifest from "../manifest.json";
import {EidolonEvents} from "@eidolon/components";

export interface ProcessPageProps {
  params: {
    processId: string
  }
}

export default async function ({params}: ProcessPageProps) {
  const processStatus = await _processHandler.getProcess(manifest.location, params.processId)
  if (!processStatus) {
    notFound()
  }

  return (
    <div style={{height: "100%"}}>
      <EidolonEvents machineUrl={processStatus.machine} agentName={processStatus.agent} processId={params.processId}/>
    </div>
  )
}
