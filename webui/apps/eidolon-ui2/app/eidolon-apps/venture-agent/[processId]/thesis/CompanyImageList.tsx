import {Box, Grid} from "@mui/material";
import {CompanyListItem} from "./CompanyListItem";
import * as React from "react";
import {Company} from "../../types";


export interface CompanyListProps {
  companies: Company[]
  selectedCompany: Company | undefined
  toggleCompany: (item: Company) => void
}

export function CompanyImageList({companies, selectedCompany, toggleCompany}: CompanyListProps) {


  const getStop = (numCols: number) => {
    numCols = Math.min(numCols, companies.length)
    return 12 / numCols
  }

  return (
    <Box
      sx={{height: '100%', width: '100%'}}
    >
      <Box
        sx={{overflowY: 'scroll', height: '100%', width: '100%', display: "flex", alignItems: "center", flexDirection: 'column'}}
      >
        <Box
          sx={{display: "flex", flexWrap: "wrap", justifyContent: "center", alignItems: "center"}}
        >
          {companies && companies.map((item) => (
            <CompanyListItem item={item} selectedCompany={selectedCompany} selectCompany={toggleCompany}/>
          ))}
        </Box>
      </Box>
    </Box>
  )
}
