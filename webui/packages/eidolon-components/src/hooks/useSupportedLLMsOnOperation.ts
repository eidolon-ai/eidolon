import {useEffect, useState} from "react";
import {OperationInfo} from "@eidolon/client";

export function useSupportedLLMsOnOperation(operation: OperationInfo) {
  const [selectedLLM, setSelectedLLM] = useState<string>("")
  useEffect(() => {
    const schema = operation.schema
    if (schema?.properties?.execute_on_cpu) {
      let property = schema?.properties?.execute_on_cpu as Record<string, any>
      if (property?.default) {
        setSelectedLLM(property.default)
      } else {
        setSelectedLLM(property?.["enum"][0])
      }
    }
  }, [operation]);

  return {
    selectedLLM,
    setSelectedLLM
  }
}
