import {useEffect, useState} from "react";
import {OperationInfo, ProcessStatus} from "@eidolon-ai/client";
import {RJSFSchema, UiSchema} from '@rjsf/utils';
import {IChangeEvent} from '@rjsf/core';
import TailwindRJSFTheme from "./rjsf-tailwind.js";

interface AgentInputFormProps {
  handleSubmit: (formJson: Record<string, any>) => void;
  operations: OperationInfo[];
  isProgram: boolean;
  processState?: ProcessStatus;
}

function getAvailableOperations(operations: OperationInfo[], processState: ProcessStatus | undefined): OperationInfo[] {
  return processState ? operations.filter((op) => processState.available_actions.includes(op.name)) : [];
}

export function AgentInputForm({handleSubmit, operations, isProgram, processState}: AgentInputFormProps) {
  const [agentOperation, setAgentOperation] = useState<number>(0);
  const [schema, setSchema] = useState<RJSFSchema>({});
  const [title, setTitle] = useState<string>("");
  const [formData, setFormData] = useState<any>({});
  const [usableOperations, setUsableOperations] = useState<OperationInfo[]>(getAvailableOperations(operations, processState));

  useEffect(() => {
    const newUsableOperations = getAvailableOperations(operations, processState);
    setUsableOperations(newUsableOperations);
    const operationInfo = newUsableOperations[0];
    if (operationInfo) {
      setAgentOperation(0);
      setSchema({...operationInfo.schema, title: undefined} as RJSFSchema);
    }
  }, [operations, processState]);

  const handleFormSubmit = (event: IChangeEvent) => {
    handleSubmit({data: event.formData, title, operation: usableOperations[agentOperation]});
  };

  const handleOperationChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const index = parseInt(event.target.value);
    setAgentOperation(index);
    const operationInfo = usableOperations[index];
    if (operationInfo) {
      setSchema({...operationInfo.schema, title: undefined} as RJSFSchema);
      setFormData({});
    }
  };

  const uiSchema: UiSchema = {
    'ui:submitButtonOptions': {norender: true}
  };

  return (
    <div className="w-full h-full flex flex-col">
      {isProgram && (
        <div className="mb-4 flex-shrink-0">
          <label htmlFor="title" className="block text-sm font-medium text-gray-700">Title</label>
          <input
            type="text"
            id="title"
            required
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
          />
        </div>
      )}
      <div className="mb-4 flex-shrink-0">
        <label htmlFor="operation" className="block text-sm font-medium text-gray-700">Operation</label>
        <select
          id="operation"
          value={usableOperations.length ? agentOperation : ''}
          onChange={handleOperationChange}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
        >
          {usableOperations.map((op, index) => (
            <option key={index} value={index}>{op.label}</option>
          ))}
        </select>
      </div>
      <div className="flex grow overflow-y-auto min-h-0 relative">
        <TailwindRJSFTheme
          schema={schema}
          uiSchema={uiSchema}
          formData={formData}
          onChange={(e: IChangeEvent<any>) => setFormData(e.formData)}
          // onSubmit={handleFormSubmit}
        />
      </div>
    </div>
  );
}