'use client'

import * as React from "react";
import {useEffect} from "react";
import {Box} from "@mui/material";
import {executeOperation, streamOperation} from "@eidolon/components/src/client-api-helpers/process-event-helper";
import {CopilotParams, useProcess} from "@eidolon/components";
import {CompanyList} from "./CompanyList";
import {Company} from "../../types";

export default function () {
  const {app, processStatus} = useProcess()
  const [companies, setCompanies] = React.useState<Company[] | undefined>(undefined)
  const appOptions = app?.params as CopilotParams

  useEffect(() => {
    if (!app || !processStatus) {
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

        // noinspection JSIgnoredPromiseFromCall
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
      let new_comp: Company = {...foundCompany, ...company};
      inCompanies[index] = new_comp
      const companiesCopy = [...inCompanies]
      setCompanies(companiesCopy)
      return new_comp
    } else {
      return company
    }
  }

  const reload = (item: Company): Promise<Company> => {
    item.loading = true
    updateCompany(item)
    const newCompanyInfo = executeOperation(app!.location, appOptions.agent, "research_company", processStatus!.process_id, {companyName: item.name})
    return newCompanyInfo.then((newItem) => {
      newItem.loading = false
      return updateCompany(newItem)
    })
  }

  if (!app || !companies) {
    return
  }

  return (
    <Box
      sx={{height: "100%"}}
    >
      <CompanyList companies={companies} reload={reload}/>
    </Box>
  )
}
