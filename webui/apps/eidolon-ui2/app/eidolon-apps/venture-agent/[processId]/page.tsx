'use client'

import * as React from "react";
import {useEffect} from "react";
import {useOperation} from "@/hooks/page_helper";
import {useRouter} from "next/navigation";
import {Company} from "../types";
import {executeOperation} from "@eidolon/components/src/client-api-helpers/process-event-helper";
import {CopilotParams} from "@eidolon/components";

export interface ProcessPageProps {
  params: {
    processId: string
  }
}

export default function ({params}: ProcessPageProps) {
  const app_name = 'venture-agent'
  const {app, error, processStatus} = useOperation(app_name, params.processId)
  const router = useRouter()
  const [companies, setCompanies] = React.useState<Company[] | undefined>(undefined)
  const appOptions = app?.params as CopilotParams

  useEffect(() => {
    if (!app) {
      return
    }
    executeOperation(app!.location, appOptions.agent, "get_companies", processStatus.process_id, {}).then((companies: Company[]) => {
      companies = companies
        .sort((a, b) => a.name.localeCompare(b.name))
        .filter((company) => company.should_research)
        .map((company) => {
          if (!company.researched_details) {
            company.loading = true
          }
          return company
        })
      setCompanies(companies)
    })
  }, []);
  if (!error && !app) {
    return <div>Loading...</div>
  }
  if (error) {
    return <div>{error}</div>
  }

  if (processStatus?.state === 'initialized') {
    router.replace(`/eidolon-apps/venture-agent/${params.processId}/portfolio`)
  } else if (processStatus && companies) {
    console.log("here")
    if (companies.filter((company) => company.should_research).length === 0) {
      router.replace(`/eidolon-apps/venture-agent/${params.processId}/choose`)
    } else {
      router.replace(`/eidolon-apps/venture-agent/${params.processId}/thesis`)
    }
  }

  return (
    <div></div>
  )
}
