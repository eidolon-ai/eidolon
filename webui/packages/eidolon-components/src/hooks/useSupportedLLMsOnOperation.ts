import {useEffect, useState} from "react"
import {OperationInfo} from "@eidolon/client"
import {CopilotParams} from "../lib/util"
import {getOperations} from "../client-api-helpers/machine-helper"

export function useSupportedLLMsOnOperation(machineURL: string, copilotParams: CopilotParams) {
  const [selectedLLM, setSelectedLLM] = useState<string>(copilotParams?.defaultLLM || "")

  function updateSelectedLLM(opInfo: OperationInfo) {
    const schema = opInfo.schema
    if (schema?.properties?.execute_on_apu) {
      let property = schema?.properties?.execute_on_apu as Record<string, any>
      if (property?.default) {
        setSelectedLLM(property.default)
      } else {
        setSelectedLLM(property?.["enum"][0])
      }
    }
  }


  useEffect(() => {
    if (copilotParams) {

      if (copilotParams.operationInfo) {
        updateSelectedLLM(copilotParams.operationInfo)
      } else {
        getOperations(machineURL, copilotParams.agent).then(ops => {
          let opInfo = ops.find(op => op.name === copilotParams.operation)
          if (opInfo) {
            copilotParams.operationInfo = opInfo
            updateSelectedLLM(opInfo)
          }
        })
      }
    }
  }, [copilotParams?.operation])

  return {
    selectedLLM,
    setSelectedLLM
  }
}
