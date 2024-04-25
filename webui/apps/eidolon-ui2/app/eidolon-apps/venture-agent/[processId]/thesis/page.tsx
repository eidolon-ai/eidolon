'use client'

import * as React from "react";
import {useEffect} from "react";
import {useOperation} from "@/hooks/page_helper";
import {Box} from "@mui/material";
import {executeOperation, streamOperation} from "@eidolon/components/src/client-api-helpers/process-event-helper";
import {CopilotParams} from "@eidolon/components";
import {useRouter} from "next/navigation";
import {CompanyList} from "./CompanyList";
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

  const appOptions = app?.params as CopilotParams

  useEffect(() => {
    if (!app) {
      return
    }

    if (processStatus.state === 'idle') {
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

        const companiesToResearch = companies.filter((company) => !company.researched_details).map((company) => company.name)

        streamOperation(app.location, appOptions.agent, "research_more_companies", processStatus.process_id, {companyNames: companiesToResearch}, (event) => {
          if (event.category === "output") {
            const newCompany = event.content as Company
            const index = companies.findIndex((c) => c.name === newCompany.name)
            const company = companies[index]!
            company.researched_details = (newCompany as Company).researched_details
            company.loading = false
            updateCompany(company, companies)
          }
        })
      })
    }
  }, [app?.location, appOptions?.agent, processStatus?.process_id]);

  const updateCompany = (company: Company, inCompanies: Company[] | undefined = undefined) => {
    inCompanies = inCompanies || companies
    if (inCompanies) {
      const index = inCompanies.findIndex((c) => c.name === company.name)
      const foundCompany = inCompanies[index]!
      inCompanies[index] = {...foundCompany, ...company}
      const companiesCopy = [...inCompanies]
      setCompanies(companiesCopy)
    }
  }

  const reload = (item: Company) => {
    item.loading = true
    updateCompany(item)
    const newCompanyInfo = executeOperation(app!.location, appOptions.agent, "research_company", processStatus.process_id, {companyName: item.name})
    newCompanyInfo.then((newItem) => {
      newItem.loading = false
      updateCompany(newItem)
    })
  }

  if (!app || !companies) {
    return <div>Loading...</div>
  }

  return (
    <Box
      sx={{height: "100%"}}
    >
      <CompanyList companies={companies} reload={reload}/>
    </Box>
  )
}
