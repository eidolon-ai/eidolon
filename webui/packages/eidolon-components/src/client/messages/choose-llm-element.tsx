'use client'

import {MenuItem, Select} from "@mui/material";

export interface ChooseLLMElementProps {
  supportedLLMs: string[] | undefined
  selectedLLM: string
  // eslint-disable-next-line no-unused-vars
  setSelectedLLM: (llm: string) => void
}

export const ChooseLLMElement = ({supportedLLMs, selectedLLM, setSelectedLLM}: ChooseLLMElementProps) => {
  if (!supportedLLMs) {
    return <></>
  } else {
    return (
      <Select
        variant={"standard"}
        value={selectedLLM}
        onChange={(event) => {
          setSelectedLLM(event.target.value as string)
        }}
        >
        {supportedLLMs.map(llm => <MenuItem key={llm} value={llm}>{llm}</MenuItem>)}
      </Select>
    )
  }
}
