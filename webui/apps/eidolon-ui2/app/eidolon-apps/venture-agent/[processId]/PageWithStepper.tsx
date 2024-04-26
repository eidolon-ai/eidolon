'use client'

import {Box, Step, StepButton, Stepper, Typography} from "@mui/material";
import * as React from "react";
import {Fragment, useEffect} from "react";
import {CopilotParams, useProcess} from "@eidolon/components";
import {usePathname} from "next/navigation";
import {Company} from "../types";
import {executeOperation} from "@eidolon/components/src/client-api-helpers/process-event-helper";

interface ChatbotLayoutProps {
  children: JSX.Element
  params: {
    processId: string
  }
}

const steps = ['Load Venture Portfolio', 'Explore Companies', 'Create Thesis'];

export default function PageWithStepper({children, params}: ChatbotLayoutProps) {
  const app_name = 'venture-agent'
  const pathName = usePathname()
  const {app, processStatus, updateProcessStatus} = useProcess()
  const [allowedStates, setAllowedStates] = React.useState<boolean[]>([true, false, false])
  const appOptions = app?.params as CopilotParams

  useEffect(() => {
    updateProcessStatus(app_name, params.processId).then((status) => {
      if (app && processStatus && processStatus.state === 'idle') {
        executeOperation(app.location, appOptions.agent, "get_companies", processStatus!.process_id, {}).then((comps: Company[]) => {
          comps.sort((a, b) => a.name.localeCompare(b.name))
          const states = [true, false, false]
          if (processStatus?.state === 'idle') {
            states[1] = true
            if (comps.filter((company) => company.should_research).length > 0) {
              states[2] = true
            }
          }
          setAllowedStates(states)
        }).catch((e) => {
          console.error(e)
        })
      }
    })
  }, [app?.location, appOptions?.agent, processStatus?.process_id, processStatus?.state]);

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

  const goToIndex = (index: number) => {
    switch (index) {
      case 0:
        window.location.href = 'portfolio'
        break
      case 1:
        window.location.href = 'choose'
        break
      case 2:
        window.location.href = 'thesis'
        break
    }
  }

  return (
    <Box sx={{width: '100%', padding: "16px", overflow: "hidden"}}>
      <Typography textAlign={"center"} sx={{margin: "16px"}} variant={"h4"}>Venture Research Tool</Typography>
      <Stepper nonLinear activeStep={activeStep} sx={{paddingBottom: '32px'}}>
        {steps.map((label, index) => {
          return (
            <Step
              key={index}
              disabled={!allowedStates[index]}
              completed={index < activeStep}
            >
              <StepButton color="inherit" onClick={() => {
                goToIndex(index)
              }}>
                {label}
              </StepButton>
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
  )
}
