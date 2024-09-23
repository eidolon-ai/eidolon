'use client'

import {CopilotPanel, CopilotParams} from "@eidolon-ai/components/client";
import * as React from "react";
import {Company} from "../../types";
import {Box, IconButton, Paper, useMediaQuery, useTheme} from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import CompanyDetailsLayout from "./company_details";
import {useSession} from "next-auth/react";
import FloatingColumns from "@/components/floating-columns";

const companyDetailChat = {
  "agent": "CompanyResearcher",
  "operation": "converse",
  "inputLabel": "How can I help you?",
  "allowSpeech": false,
  "speechAgent": "speech_agent",
  "speechOperation": "speech_to_text"
} as CopilotParams

export interface CompanyDetailChatProps {
  machineURL: string
  company: Company
  setSelectedCompany: (company: Company | undefined) => void
  reloadCompanies: () => void
}

export default function CompanyDetailChat({company, reloadCompanies, machineURL, setSelectedCompany}: CompanyDetailChatProps) {
  const theme = useTheme();
  const matches = useMediaQuery(theme.breakpoints.up('lg'));
  const {data: session} = useSession()

  return (
    <FloatingColumns rightVisible={company.researched_details != undefined}
                     left={(
                       <Paper sx={{
                         height: "100%",
                         width: "100%",
                         display: "flex",
                         flexDirection: "column",
                         overflow: "hidden",
                       }}>
                         <IconButton onClick={() => setSelectedCompany(undefined)} sx={{alignSelf: 'flex-end'}}><CloseIcon/></IconButton>
                         <CompanyDetailsLayout refreshResearch={(company) => {
                           reloadCompanies()
                         }} company={company}/>
                       </Paper>
                     )}
                     right={(matches) => (
                       <CopilotPanel
                         sx={matches ? {
                           borderLeft: "1px solid black",
                           paddingLeft: "16px"
                         } : {
                           borderTop: "1px solid black",
                           paddingTop: "16px"
                         }}
                         machineUrl={machineURL}
                         processId={company.researched_details!.process_id}
                         copilotParams={companyDetailChat}
                         userName={session?.user?.name}
                         userImage={session?.user?.image}
                         afterExecute={reloadCompanies}
                       />
                     )
                     }
    />
  )
}
