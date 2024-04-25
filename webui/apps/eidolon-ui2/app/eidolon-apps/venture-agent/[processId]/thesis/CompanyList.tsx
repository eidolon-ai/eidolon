import {Box, Grid} from "@mui/material";
import {CompanyListItem} from "./CompanyListItem";
import * as React from "react";
import {Company} from "../../types";
import CompanyDetailsLayout from "./company_details";


export interface CompanyListProps {
  companies: Company[]
  reload: (item: Company) => void
}

export function CompanyList({companies, reload}: CompanyListProps) {
  const [selectedCompany, setSelectedCompany] = React.useState<Company | undefined>(undefined)

  const toggleCompany = (company: Company) => {
    if (selectedCompany?.name === company.name) {
      setSelectedCompany(undefined)
    } else {
      setSelectedCompany(company)
    }
  }

  const getStop = (numCols: number) => {
    numCols = Math.min(numCols, companies.length)
    return 12 / numCols
  }

  return (
    <Box
      sx={{height: '100%', width: '100%'}}
    >
      <Box
        sx={{overflowY: 'scroll', height: selectedCompany ? '60%' : '100%', width: '100%', display: "flex", alignItems: "center", flexDirection: 'column'}}
      >
        <Grid
          sx={{width: '65vw'}}
          container spacing={2}
        >
          {companies && companies.map((item) => (
            <Grid item xs={getStop(1)} sm={getStop(2)} md={getStop(3)} lg={getStop(4)} xl={getStop(6)} key={item.name}
                  sx={{display: 'flex', justifyContent: 'center'}}
            >
              <CompanyListItem item={item} selectedCompany={selectedCompany} selectCompany={toggleCompany}/>
            </Grid>
          ))}
        </Grid>
      </Box>
      {selectedCompany && (
        <Box
          sx={{height: '40%', borderTop: '2px solid #ccc', width: '100%', marginTop: '16px'}}
        >
          <CompanyDetailsLayout refreshResearch={reload} company={selectedCompany}/>
        </Box>
      )}
    </Box>
  )
}
