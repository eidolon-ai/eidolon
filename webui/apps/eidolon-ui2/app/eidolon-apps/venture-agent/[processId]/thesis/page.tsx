'use client'

import * as React from "react";
import {useEffect} from "react";
import {Box} from "@mui/material";
import {executeOperation, streamOperation} from "@eidolon/components/client";
import {CopilotParams, useProcess} from "@eidolon/components/client";
import {CompanyImageList} from "./CompanyImageList";
import {Company} from "../../types";
import CompanyDetailChat from "./company-detail-chat";


export default function () {
  const {app, processStatus} = useProcess()
  const [companies, setCompanies] = React.useState<Company[] | undefined>(undefined)
  const appOptions = app?.params as CopilotParams
  const [selectedCompany, setSelectedCompany] = React.useState<Company | undefined>(undefined)
  const [loading, setLoading] = React.useState<boolean>(false)

  const loadCompanies = async () => {
    return executeOperation(app!.location, appOptions.agent, "get_companies", processStatus!.process_id, {}).then((companies: Company[]) => {
      if (!companies) {
        companies = []
      }
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
      if (selectedCompany) {
        setSelectedCompany(companies.find((c) => c.name === selectedCompany.name))
      }
      return companies
    })
  }

  useEffect(() => {
    if (!app || !processStatus) {
      return
    }

    if (!loading) {
      setLoading(true)
      if (processStatus.state === 'idle') {
        loadCompanies().then((companies: Company[]) => {
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
      setLoading(false)
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

  const toggleCompany = (company: Company) => {
    if (selectedCompany?.name === company.name) {
      setSelectedCompany(undefined)
    } else {
      setSelectedCompany(company)
    }
  }

  if (!app || !companies) {
    return
  }

  return (
    <Box
      sx={{height: "100%", display: "flex", flexDirection: "row", maxWidth: "100%"}}
    >
      {!selectedCompany && (
        <CompanyImageList companies={companies} selectedCompany={selectedCompany} toggleCompany={toggleCompany}/>
      )}
      {selectedCompany && (
        <CompanyDetailChat company={selectedCompany} reloadCompanies={loadCompanies} machineURL={app.location} setSelectedCompany={setSelectedCompany}/>
      )}

    </Box>
  )
}
