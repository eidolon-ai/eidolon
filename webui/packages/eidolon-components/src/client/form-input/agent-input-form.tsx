import {useEffect, useState} from "react";
import {OperationInfo} from "@eidolon-ai/client";
import {RJSFSchema, UiSchema} from '@rjsf/utils';
import TailwindRJSFTheme from "./rjsf-tailwind.js";
import {useProcess} from "../hooks/process_context.js";
import {useApp} from "../hooks/app-context.js";
import StyledSelect from "./styled-select.js";

interface AgentInputFormProps {
  formData: unknown;
  setFormData: (data: unknown) => void;
  operations: OperationInfo[];
  agentOperation?: string
  setAgentOperation: (operation: string | undefined) => void;
  onSubmit: () => void
}

export function AgentInputForm({formData, setFormData, operations, agentOperation, setAgentOperation, onSubmit}: AgentInputFormProps) {
  const [schema, setSchema] = useState<RJSFSchema>({});
  const [usableOperations, setUsableOperations] = useState<OperationInfo[]>([]);
  const {processStatus: processState} = useProcess()
  const {app} = useApp()

  useEffect(() => {
    if (app && processState) {
      const newUsableOperations = operations.filter((op) => processState.available_actions.includes(op.name));
      setUsableOperations(newUsableOperations);
      let operationInfo = agentOperation ? newUsableOperations.find(p => p.name == agentOperation) : newUsableOperations[0];
      if (!operationInfo) {
        operationInfo = newUsableOperations.length > 0 ? newUsableOperations[0] : undefined
      }
      if (operationInfo) {
        if (agentOperation != operationInfo.name) {
          setAgentOperation(operationInfo.name);
        }
        setSchema({...operationInfo.schema, title: undefined} as RJSFSchema);
      }
    }
  }, [operations, processState, app]);

  const handleOperationChange = (oper: string) => {
    const operationInfo = usableOperations.find(op => op.name === oper)
    setAgentOperation(operationInfo?.name);
    if (operationInfo) {
      setSchema({...operationInfo.schema, title: undefined} as RJSFSchema);
      setFormData({});
    }
  };

  const uiSchema: UiSchema = {
    'ui:submitButtonOptions': {norender: true}
  };
  return (
    <div className="w-full h-full flex flex-col p-4 space-y-2">
      <div>
        <label htmlFor="operation" className="block text-sm font-medium text-gray-700 mb-1">
          Operation
        </label>
        <StyledSelect options={usableOperations.map(op => op.name)} value={agentOperation!} onChange={handleOperationChange}/>
      </div>
      <div className="flex-grow overflow-y-auto min-h-0">
        {schema && schema.type && (
          <TailwindRJSFTheme
            schema={schema}
            uiSchema={uiSchema}
            formData={formData}
            onSubmit={onSubmit}
            onChange={(e) => setFormData(e.formData)}
          />
        )}
      </div>
    </div>
  );
}