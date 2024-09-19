import {useEffect, useState} from "react";
import {OperationInfo, ProcessStatus} from "@eidolon-ai/client";
import {RJSFSchema, UiSchema} from '@rjsf/utils';
import {IChangeEvent} from '@rjsf/core';
import TailwindRJSFTheme from "./rjsf-tailwind.js";

interface AgentInputFormProps {
  handleSubmit: (formJson: Record<string, any>) => void;
  operations: OperationInfo[];
  selectedOperation?: string
  processState?: ProcessStatus;
}

function getAvailableOperations(operations: OperationInfo[], processState: ProcessStatus | undefined): OperationInfo[] {
  return processState ? operations.filter((op) => processState.available_actions.includes(op.name)) : [];
}

export function AgentInputForm({handleSubmit, operations, selectedOperation, processState}: AgentInputFormProps) {
  const [agentOperation, setAgentOperation] = useState<string | undefined>(selectedOperation);
  const [schema, setSchema] = useState<RJSFSchema>({});
  const [title, setTitle] = useState<string>("");
  const [formData, setFormData] = useState<any>({});
  const [usableOperations, setUsableOperations] = useState<OperationInfo[]>(getAvailableOperations(operations, processState));

  useEffect(() => {
    const newUsableOperations = getAvailableOperations(operations, processState);
    setUsableOperations(newUsableOperations);
    const operationInfo = selectedOperation ? newUsableOperations.find(p => p.name == selectedOperation): newUsableOperations[0];
    if (operationInfo) {
      setAgentOperation(newUsableOperations[0]?.name);
      setSchema({...operationInfo.schema, title: undefined} as RJSFSchema);
    }
  }, [operations, processState]);

  const handleFormSubmit = (event: IChangeEvent) => {
    handleSubmit({data: event.formData, title, operation: agentOperation});
  };

  const handleOperationChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const operationInfo = usableOperations.find(op => op.name === event.target.value)
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
        <select
          id="operation"
          defaultValue={agentOperation}
          onChange={handleOperationChange}
          className="w-full px-3 py-2 rounded-md border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
        >
          {usableOperations.map((op, index) => (
            <option key={op.name} value={op.name} className="py-1">
              {op.label}
            </option>
          ))}
        </select>
      </div>
      <div className="flex-grow overflow-y-auto min-h-0">
        <TailwindRJSFTheme
          schema={schema}
          uiSchema={uiSchema}
          formData={formData}
          onChange={(e) => setFormData(e.formData)}
        />
      </div>
    </div>
  );
}