'use client'

import * as React from "react";
import {useEffect} from "react";
import {Box} from "@mui/material";
import {executeOperation} from "@eidolon/components/src/client-api-helpers/process-event-helper";
import {CopilotPanel, CopilotParams, useProcess, useProcesses} from "@eidolon/components";
import EnhancedTable from "./company_list";
import {useRouter} from "next/navigation";
import {Company, Thesis} from "../../types";
import FloatingColumns from "@/components/floating-columns";
import {useSession} from "next-auth/react";

const findCompanyChat = {
  "agent": "CompanyFinder",
  "operation": "converse",
  "inputLabel": "Use the chat to find companies. When you find a company say 'add it to the list'.",
  "allowSpeech": true,
  "speechAgent": "speech_agent",
  "speechOperation": "speech_to_text"
} as CopilotParams

export default function () {
  const {app, processStatus} = useProcess()
  const [thesis, setThesis] = React.useState<Thesis | undefined>(undefined)
  const [companies, setCompanies] = React.useState<Company[] | undefined>(undefined)
  const [loading, setLoading] = React.useState<boolean>(false)
  const router = useRouter()
  const appOptions = app?.params as CopilotParams
  const {data: session} = useSession()
  const {updateProcesses} = useProcesses()

  const updateCompanies = () => {
    return executeOperation(app!.location, appOptions.agent, "get_companies", processStatus!.process_id, {}).then((inCompanies) => {
      const companies = (inCompanies || []) as Company[]
      (companies as Company[]).sort((a, b) => a.name.localeCompare(b.name))
      setCompanies(companies)
    })
  }

  useEffect(() => {
    if (!app || !processStatus) {
      return
    }
    if (processStatus.state === "initialized" && !loading) {
      setLoading(true)
      executeOperation(app!.location, app!.params.agent, "start_thesis", processStatus!.process_id, {}).then((response) => {
        setThesis(response.data)
        setCompanies([])
      }).finally(() => {
        setLoading(false)
      })
    } else if (processStatus.state === 'idle' && !loading) {
      setLoading(true)
      executeOperation(app!.location, appOptions.agent, "get_thesis", processStatus.process_id, {}).then((thesis) => {
        setThesis(thesis as Thesis)
        console.log(thesis)
        return updateCompanies()
      }).catch((e) => {
        console.error(e)
      }).finally(() => {
        setLoading(false)
      })
    }
  }, [app?.location, appOptions?.agent, processStatus?.process_id]);

  if (!app || !companies || !thesis || !processStatus || processStatus.state === 'initialized') {
    return
  }

  const afterExecute = (payload: string | Record<string, any>) => {
    updateCompanies()
    if (!processStatus?.title) {
      executeOperation(app.location, app.params.agent, "generateTitle", processStatus.process_id, {body: payload}).then(() => {
        updateProcesses(app.location).then()
      })
    }
  }

  const markCompanies = (companies: readonly string[]) => {
    executeOperation(app!.location, appOptions.agent, "mark_companies_for_research", processStatus!.process_id, {companies}).then(() => {
      router.push('thesis')
    })
  }

  return (
    <FloatingColumns rightVisible={true} left={(
      <Box
        sx={{display: "flex", alignItems: "center", justifyContent: "center", height: "100%", width: "100%", overflow: "hidden"}}
      >
        <EnhancedTable companies={companies} selectItems={markCompanies}/>
      </Box>
    )} right={(
      <CopilotPanel
        machineUrl={app.location}
        processId={thesis!.companyFinderPID}
        copilotParams={findCompanyChat}
        userName={session?.user?.name}
        userImage={session?.user?.image}
        afterExecute={afterExecute}
      />)}/>
  )
}
