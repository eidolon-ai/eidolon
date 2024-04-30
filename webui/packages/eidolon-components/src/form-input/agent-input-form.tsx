'use client'

import validator from '@rjsf/validator-ajv8';
import {Form} from "@rjsf/mui";
import {useEffect, useState} from "react";
import {FormControl, MenuItem, Select, SelectChangeEvent, TextField} from "@mui/material";
import {OperationInfo, ProcessStatus} from "@eidolon/client";

const log = (type: any) => console.log.bind(console, type);

interface AgentInputFormProps {
  // eslint-disable-next-line no-unused-vars
  handleSubmit: (formJson: Record<string, any>) => void
  operations: OperationInfo[]
  isProgram: boolean
  processState?: ProcessStatus
}


function getAvailableOperations(operations: OperationInfo[], processState: ProcessStatus | undefined): OperationInfo[] {
  if (processState) {
    return operations.filter((op) => processState.available_actions.includes(op.name))
  } else {
    return []
  }
}

export function AgentInputForm({handleSubmit, operations, isProgram, processState}: AgentInputFormProps) {
  const [agentOperation, setAgentOperation] = useState<number>(0);
  // Form state
  const [schema, setSchema] = useState<any>({})
  const [title, setTitle] = useState<string>("")
  const [formData, setFormData] = useState<any>({})

  // the next line filters operations that are not usable as defined by processState.available_actions
  const [usableOperations, setUsableOperations] = useState<OperationInfo[]>(getAvailableOperations(operations, processState))

  useEffect(() => {
    setUsableOperations(getAvailableOperations(operations, processState))
    const operationInfo = usableOperations[0]
    if (operationInfo) {
      setAgentOperation(0)
      delete operationInfo.schema?.title
      setSchema(operationInfo.schema)
    }
    return () => {}
  }, [operations, processState])

  // @ts-ignore
  return (
    <form
      id={"agent-input-form"}
      onSubmit={(event) => {
        event.preventDefault();
        handleSubmit({data: formData, title: title, operation: usableOperations[agentOperation]})
      }}
    >
      <FormControl variant={"standard"} fullWidth={true}>
        {isProgram && (
          <TextField
            sx={{marginBottom: '16px'}}
            label={"Title"}
            required={true}
            value={title}
            onChange={(event) => setTitle(event.target.value)}
          />
        )}
        <Select
          labelId={"op_label"}
          label={"Operation"}
          value={usableOperations?.length ? agentOperation : ''}
          onChange={(event: SelectChangeEvent<number>) => {
            let operationInfo = usableOperations[event.target.value as number];
            setAgentOperation(event.target.value as number);
            if (operationInfo) {
              delete operationInfo.schema?.title
              setSchema(operationInfo.schema)
            }
          }}
        >
          {usableOperations.map((op, index) => (
            <MenuItem
              key={index}
              value={index}
            >{op.label}</MenuItem>
          ))}
        </Select>
        <div style={{width: '90%'}}>
          <Form
            id={"agent-input-form"}
            tagName={"div"}
            schema={schema}
            liveValidate={true}
            // @ts-ignore
            validator={validator}
            onChange={(data) => {
              setFormData(data.formData)
            }}
            onError={log('errors')}
            uiSchema={{'ui:submitButtonOptions': {norender: true}}}
          >
          </Form>
        </div>
      </FormControl>
    </form>
  )
}
