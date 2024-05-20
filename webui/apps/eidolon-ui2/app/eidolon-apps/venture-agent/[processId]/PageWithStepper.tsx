'use client'

import {Box, Step, StepButton, Stepper} from "@mui/material";
import * as React from "react";
import {Fragment, useEffect, useRef} from "react";
import {usePathname} from "next/navigation";
import {useProcess} from "@eidolon/components";

interface ChatbotLayoutProps {
  children: JSX.Element
  params: {
    processId: string
  }
}

const steps = ['Explore Companies', 'Research', 'Export'];

export default function PageWithStepper({children, params}: ChatbotLayoutProps) {
  const app_name = 'venture-agent'
  const pathName = usePathname()
  const {processStatus, updateProcessStatus} = useProcess()
  const running = useRef(false)

  useEffect(() => {
    if (!running.current && !processStatus && params?.processId) {
      running.current = true
      updateProcessStatus(app_name, params.processId).finally(() => {
        // running.current = false
      })
    }
  }, [processStatus?.state]);

  let activeStep = -1
  switch (pathName.slice(pathName.lastIndexOf('/') + 1)) {
    case 'choose':
      activeStep = 0
      break
    case 'thesis':
      activeStep = 1
      break
  }

  const goToIndex = (index: number) => {
    switch (index) {
      case 0:
        window.location.href = 'choose'
        break
      case 1:
        window.location.href = 'thesis'
        break
    }
  }

  if (!processStatus) {
    return <Box>Loading...</Box>
  }

  return (
    <Box sx={{width: '100%', padding: "16px", overflow: "hidden"}}>
      <Stepper nonLinear activeStep={activeStep} sx={{paddingBottom: '32px'}}>
        {steps.map((label, index) => {
          return (
            <Step
              key={index}
              disabled={false}
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
        <Box sx={{height: 'calc(100% - 58px)', width: '100%'}}>
          {children}
        </Box>
      </Fragment>
    </Box>
  )
}
