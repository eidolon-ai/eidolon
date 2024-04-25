'use client'

import {Box, Step, StepLabel, Stepper, Typography} from "@mui/material";
import * as React from "react";
import {Fragment} from "react";
import {ProcessProvider} from "@eidolon/components";
import {usePathname} from "next/navigation";

interface ChatbotLayoutProps {
  children: JSX.Element
}

const steps = ['Load Venture Portfolio', 'Explore Companies', 'Filter by Thesis', 'Research'];

export default function ChatbotLayout({children}: ChatbotLayoutProps) {
  const pathName = usePathname()

  let activeStep = -1
  switch (pathName.slice(pathName.lastIndexOf('/') + 1)) {
    case 'portfolio':
      activeStep = 0
      break
    case 'choose':
      activeStep = 1
      break
    case 'thesis':
      activeStep = 2
      break
  }

  return (
    <ProcessProvider>
      <Box sx={{width: '100%', padding: "16px", overflow: "hidden"}}>
        <Typography textAlign={"center"} sx={{margin: "16px"}} variant={"h4"}>Venture Research Tool</Typography>
        <Stepper activeStep={activeStep} sx={{paddingBottom: '32px'}}>
          {steps.map((label, index) => {
            const stepProps: { completed?: boolean } = {};
            return (
              <Step key={index} {...stepProps}>
                <StepLabel>
                  {label}
                </StepLabel>
              </Step>
            );
          })}
        </Stepper>
        <Fragment>
          <Box sx={{height: 'calc(100vh - 210px)', width: '100%'}}>
              {children}
          </Box>
        </Fragment>
      </Box>
    </ProcessProvider>
  )
}
