'use client'

import * as React from "react";
import {useEffect} from "react";
import {useOperation} from "@/hooks/page_helper";
import {Box} from "@mui/material";
import {executeOperation} from "@eidolon/components/src/client-api-helpers/process-event-helper";
import {CopilotParams} from "@eidolon/components";
import EnhancedTable from "./select_all_transfer_list";
import {useRouter} from "next/navigation";
import {Company} from "../../types";

export interface ProcessPageProps {
  params: {
    processId: string
  }
}

export default function ({params}: ProcessPageProps) {
  const app_name = 'venture-agent'
  const {app, error, processStatus} = useOperation(app_name, params.processId)
  const [companies, setCompanies] = React.useState<Company[] | undefined>(undefined)
  const router = useRouter()

  const appOptions = app?.params as CopilotParams
  useEffect(() => {
    if (!app) {
      return
    }

    console.log(processStatus.state)

    if (processStatus.state === 'idle') {
      executeOperation(app!.location, appOptions.agent, "get_companies", processStatus.process_id, {}).then((companies) => {
        (companies as Company[]).sort((a, b) => a.name.localeCompare(b.name))
        setCompanies(companies)
      }).catch((e) => {
        console.error(e)
      })
    }
  }, [app?.location, appOptions?.agent, processStatus?.process_id]);

  if (!app || !companies) {
    return <div>Loading...</div>
  }

  const markCompanies = (companies: readonly string[]) => {
    executeOperation(app!.location, appOptions.agent, "mark_companies_for_research", processStatus.process_id, {companies}).then(() => {
      router.push('thesis')
    })
  }


  return (
    <Box
      sx={{display: "flex", alignItems: "center", justifyContent: "center"}}
    >
      <Box
        sx={{width: '65vw'}}
      >
        <EnhancedTable companies={companies} selectItems={markCompanies}/>
      </Box>
    </Box>
  )
}
