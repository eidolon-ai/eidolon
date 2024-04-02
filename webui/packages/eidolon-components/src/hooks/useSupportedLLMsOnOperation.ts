import {useEffect, useState} from "react";
import {EidolonClient} from "@eidolon/client";
import {OpenAPIV3_1} from "openapi-types";

export function useSupportedLLMsOnOperation(machineUrl: string, agent: string, operation: string) {
  const [supportedLLMs, setSupportedLLMs] = useState<string[] | undefined>(undefined)
  const [selectedLLM, setSelectedLLM] = useState<string>("")

  useEffect(() => {
    const client = new EidolonClient(machineUrl)
    client.getActions().then(Object.values).then(operations => operations.filter(action => action.name === operation && action.agent === agent)).then(operations => {
      if (operations.length === 1) {
        const schema = operations[0].schema as OpenAPIV3_1.SchemaObject
        if (schema?.properties?.execute_on_cpu) {
          let property = schema?.properties?.execute_on_cpu as Record<string, any>
          setSupportedLLMs(property?.["enum"] as string[])
          if (property?.default) {
            setSelectedLLM(property.default)
          } else {
            setSelectedLLM(property?.["enum"][0])
          }
        }
      }
    })

  }, [machineUrl, agent, operation]);

  return {
    supportedLLMs,
    selectedLLM,
    setSelectedLLM
  }
}
