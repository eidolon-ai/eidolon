import React from 'react';
import {FieldProps, FieldTemplateProps, getTemplate, ObjectFieldTemplateProps, RJSFSchema, UiSchema, WidgetProps,} from '@rjsf/utils';
import validator from '@rjsf/validator-ajv8';
import {IChangeEvent, ThemeProps, withTheme} from '@rjsf/core';

// Custom widgets
const TextWidget: React.FC<WidgetProps> = (props) => {
  const { id, required, readonly, disabled, value, onChange, onBlur, onFocus, autofocus, options } = props;
  return (
    <input
      id={id}
      className={`mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50 ${readonly || disabled ? 'bg-gray-100' : ''}`}
      type={options.inputType || 'text'}
      required={required}
      disabled={disabled || readonly}
      value={value || ''}
      onChange={(event) => onChange(event.target.value)}
      onBlur={onBlur && ((event) => onBlur(id, event.target.value))}
      onFocus={onFocus && ((event) => onFocus(id, event.target.value))}
      autoFocus={autofocus}
    />
  );
};

const CheckboxWidget: React.FC<WidgetProps> = (props) => {
  const { id, value, required, readonly, disabled, onChange, label } = props;
  return (
    <div className="flex items-center">
      <input
        id={id}
        type="checkbox"
        className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
        checked={value || false}
        required={required}
        disabled={disabled || readonly}
        onChange={(event) => onChange(event.target.checked)}
      />
      <label htmlFor={id} className="ml-2 block text-sm text-gray-900">
        {label}
      </label>
    </div>
  );
};

// Custom fields
const TitleField: React.FC<FieldProps> = ({ title, required }) => (
  <h5 className="text-lg font-medium leading-6 text-gray-900 mb-2">
    {title}
    {required && <span className="text-red-500 ml-1">*</span>}
  </h5>
);

const DescriptionField: React.FC<FieldProps> = ({ description }) => (
  <p className="mt-1 text-sm text-gray-600">{description}</p>
);

// Theme
const Theme: ThemeProps = {
  widgets: {
    TextWidget,
    CheckboxWidget,
  },
  fields: {
    TitleField,
    DescriptionField,
  },
  templates: {
    FieldTemplate: (props: FieldTemplateProps) => {
      const { id, children, displayLabel, label, required, rawErrors, help } = props;
      return (
        <div className="mb-4">
          {displayLabel && (
            <label htmlFor={id} className="block text-sm font-medium text-gray-700">
              {label}
              {required && <span className="text-red-500 ml-1">*</span>}
            </label>
          )}
          {children}
          {rawErrors && rawErrors.map((error: string, i: number) => (
            <p key={i} className="mt-1 text-sm text-red-600">{error}</p>
          ))}
          {help && <p className="mt-1 text-sm text-gray-500">{help}</p>}
        </div>
      );
    },
    ObjectFieldTemplate: (props: ObjectFieldTemplateProps) => {
      const { properties, title, description, uiSchema, registry } = props;
      const TitleFieldTemplate = getTemplate<'TitleFieldTemplate'>('TitleFieldTemplate', registry, uiSchema);
      const DescriptionFieldTemplate = getTemplate<'DescriptionFieldTemplate'>('DescriptionFieldTemplate', registry, uiSchema);
      return (
        <div>
          {title && (
            <TitleFieldTemplate
              id={`${props.idSchema.$id}-title`}
              title={title}
              required={props.required}
              registry={registry}
              schema={props.schema}
            />
          )}
          {description && (
            <DescriptionFieldTemplate
              id={`${props.idSchema.$id}-description`}
              description={description}
              registry={registry}
              schema={props.schema}
            />
          )}
          {properties.map((prop) => (
            <div key={prop.name} className="mb-4">
              {prop.content}
            </div>
          ))}
        </div>
      );
    },
  },
};

const Form = withTheme(Theme);

interface TailwindRJSFThemeProps {
  schema: RJSFSchema;
  uiSchema?: UiSchema;
  formData?: any;
  onChange: (data: IChangeEvent<any, RJSFSchema, any>, id: string | undefined) => void;
}

const TailwindRJSFTheme: React.FC<TailwindRJSFThemeProps> = ({ schema, uiSchema, formData, onChange }) => {
  return (
    <Form
      schema={schema}
      uiSchema={uiSchema}
      formData={formData}
      onChange={onChange}
      validator={validator as any}
    />
  );
};

export default TailwindRJSFTheme;