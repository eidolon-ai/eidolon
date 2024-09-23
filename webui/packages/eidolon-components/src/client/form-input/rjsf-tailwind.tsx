import React from 'react';
import {
  ADDITIONAL_PROPERTY_FLAG,
  ArrayFieldTemplateItemType,
  ArrayFieldTemplateProps,
  DescriptionFieldProps,
  ErrorListProps,
  FieldTemplateProps,
  IconButtonProps,
  ObjectFieldTemplateProps,
  RJSFSchema,
  SubmitButtonProps,
  TitleFieldProps,
  UiSchema,
  WidgetProps,
  WrapIfAdditionalTemplateProps,
} from '@rjsf/utils';
import validator from '@rjsf/validator-ajv8';
import {IChangeEvent, ThemeProps, withTheme} from '@rjsf/core';
import {PlusCircle, XCircle, ChevronUp, ChevronDown, AlertCircle} from 'lucide-react';

// Custom widgets
const IconButton: React.FC<IconButtonProps> = (props) => {
  const {icon, className, ...otherProps} = props;
  return (
    <button
      className={`p-1 rounded-full transition-colors ${className}`}
      {...otherProps}
    >
      {icon}
    </button>
  );
};

const AddButton: React.FC<IconButtonProps> = (props) => (
  <IconButton
    {...props}
    className="text-green-500 hover:text-green-600"
    icon={<PlusCircle size={20}/>}
  />
);

const RemoveButton: React.FC<IconButtonProps> = (props) => (
  <IconButton
    {...props}
    className="text-red-500 hover:text-red-600"
    icon={<XCircle size={20}/>}
  />
);

const MoveUpButton: React.FC<IconButtonProps> = (props) => (
  <IconButton
    {...props}
    className="text-gray-500 hover:text-gray-600"
    icon={<ChevronUp size={20}/>}
  />
);

const MoveDownButton: React.FC<IconButtonProps> = (props) => (
  <IconButton
    {...props}
    className="text-gray-500 hover:text-gray-600"
    icon={<ChevronDown size={20}/>}
  />
);

// ErrorList Template
const ErrorListTemplate: React.FC<ErrorListProps> = ({errors}) => (
  <div className="bg-red-50 border-l-4 border-red-400 p-4 mb-4">
    <div className="flex">
      <div className="flex-shrink-0">
        <XCircle className="h-5 w-5 text-red-400"/>
      </div>
      <div className="ml-3">
        <h3 className="text-sm font-medium text-red-800">There were errors with your submission</h3>
        <div className="mt-2 text-sm text-red-700">
          <ul className="list-disc pl-5 space-y-1">
            {errors.map((error, i) => (
              <li key={i}>{error.stack}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  </div>
);

// TitleField Template
const TitleFieldTemplate: React.FC<TitleFieldProps> = ({id, title, required}) => (
  <h5 id={id} className="text-lg font-semibold text-gray-900 mb-2">
    {title}
    {required && <span className="text-red-500 ml-1">*</span>}
  </h5>
);

// DescriptionField Template
const DescriptionFieldTemplate: React.FC<DescriptionFieldProps> = ({id, description}) => (
  <p id={id} className="mt-1 text-sm text-gray-500">{description}</p>
);

// WrapIfAdditional Template
const WrapIfAdditionalTemplate: React.FC<WrapIfAdditionalTemplateProps> = (props) => {
  const {registry, classNames, style, children, disabled, id, label, onDropPropertyClick, onKeyChange, readonly, required, schema} = props;
  const additional = schema.hasOwnProperty(ADDITIONAL_PROPERTY_FLAG);

  if (!additional) {
    return <div className={classNames} style={style}>{children}</div>;
  }

  return (
    <div className={`${classNames} flex flex-col sm:flex-row items-start sm:items-center space-y-2 sm:space-y-0 sm:space-x-2 mb-2`} style={style}>
      <input
        type="text"
        className={`flex-grow px-3 py-2 text-gray-700 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400 ${required ? 'border-red-500' : 'border-gray-300'}`}
        id={`${id}-key`}
        onBlur={(event) => {
          if (event.target.value.trim() !== '') {
            onKeyChange(event.target.value);
          } else {
            console.warn('Key cannot be empty');
          }
        }}
        defaultValue={label}
        required={required}
      />
      <div className="flex-grow">{children}</div>
      <RemoveButton
        disabled={disabled || readonly}
        onClick={() => onDropPropertyClick(label)}
        className="mt-2 sm:mt-0"
        registry={registry}
      />
    </div>
  );
};

// Array field template
const ArrayFieldTemplate: React.FC<ArrayFieldTemplateProps> = (props: ArrayFieldTemplateProps) => {
  const {title, items, canAdd, onAddClick, registry} = props;
  return (
    <div className="space-y-2">
      <div className={'flex flex-row justify-between items-center'}>
        {title && (
          <TitleFieldTemplate
            id={`${props.idSchema.$id}-title`}
            title={title}
            required={props.required}
            registry={registry}
            schema={props.schema}
          />
        )}
        {canAdd && (
          <AddButton
            onClick={onAddClick}
            className="mt-2"
            registry={registry}
          />
        )}

      </div>
      <div className="space-y-2">
        {items.map((element: ArrayFieldTemplateItemType) => (
          <div key={element.key} className="flex items-center space-x-2 p-2 bg-gray-50 rounded-md">
            <div className="flex-grow">{element.children}</div>
            <div className="flex space-x-1">
              {element.hasMoveUp && (
                <MoveUpButton
                  onClick={element.onReorderClick(element.index, element.index - 1)}
                  registry={registry}
                />
              )}
              {element.hasMoveDown && (
                <MoveDownButton
                  onClick={element.onReorderClick(element.index, element.index + 1)}
                  registry={registry}
                />
              )}
              {element.hasRemove && (
                <RemoveButton
                  onClick={element.onDropIndexClick(element.index)}
                  registry={registry}
                />
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
// Updated FieldTemplate with improved spacing and layout
const FieldTemplate: React.FC<FieldTemplateProps> = (props) => {
  const {id, children, displayLabel, label, required, rawErrors, schema, uiSchema} = props;
  const widthClass = schema.type === "object" ? 'w-full' : '';
  const isRoot = uiSchema?.['ui:field'] === 'root';

  return (
    <div className={`${isRoot ? '' : 'p-2'} ${widthClass} flex flex-col justify-center`}>
        {displayLabel && (
          <label htmlFor={id} className="block text-sm font-medium text-gray-700 mb-1">
            {label}
            {required && <span className="text-red-500 ml-1">*</span>}
          </label>
        )}
        <div className={displayLabel ? 'mt-1' : ''}>{children}</div>
        {rawErrors && rawErrors.length > 0 && (
          <div className="mt-2 text-sm text-red-600">
            <div className="flex items-center">
              <AlertCircle className="h-4 w-4 mr-1"/>
              <ul>
                {rawErrors.map((error: string, i: number) => (
                  <li key={i}>{error}</li>
                ))}
              </ul>
            </div>
          </div>
        )}
    </div>
  );
};

// Updated ObjectFieldTemplate for better structure
const ObjectFieldTemplate: React.FC<ObjectFieldTemplateProps> = (props) => {
  const {properties, title, description, uiSchema} = props;
  const isRoot = uiSchema?.['ui:field'] === 'root';

  return (
    <div className={`w-full bg-white ${isRoot ? '' : 'shadow-sm rounded-lg p-2'}`}>
      {title && <h3 className="text-lg font-semibold text-gray-900 mb-2">{title}</h3>}
      {description && <p className="text-sm text-gray-500 mb-4">{description}</p>}
      <div className={`flex flex-wrap -mx-2 w-full`}>
        {properties.map((prop) => (
          <React.Fragment key={prop.name}>{prop.content}</React.Fragment>
        ))}
      </div>
    </div>
  );
};
// Updated widgets with consistent styling
const TextWidget: React.FC<WidgetProps> = (props) => {
  const {id, required, readonly, disabled, value, onChange, onBlur, options} = props;
  return (
    <input
      id={id}
      className={`w-full px-3 py-2 text-gray-700 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400 ${
        readonly || disabled ? 'bg-gray-100' : 'bg-white'
      }`}
      type={options.inputType || 'text'}
      required={required}
      disabled={disabled || readonly}
      value={value || ''}
      onChange={(event) => onChange(event.target.value)}
      onBlur={(event) => {
        if (onBlur) {
          onBlur(id, event.target.value);
        }
      }}
    />
  );
};

const CheckboxWidget: React.FC<WidgetProps> = (props) => {
  const {id, value, required, readonly, disabled, onChange, label} = props;
  return (
    <div className="flex items-center">
      <input
        id={id}
        type="checkbox"
        className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
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

// Theme
const Theme: ThemeProps = {
  widgets: {
    TextWidget,
    CheckboxWidget,
  },
  templates: {
    ButtonTemplates: {
      AddButton,
      RemoveButton,
      MoveUpButton,
      MoveDownButton,
    },
    ErrorListTemplate,
    FieldTemplate,
    ObjectFieldTemplate,
    ArrayFieldTemplate,
    TitleFieldTemplate,
    DescriptionFieldTemplate,
    WrapIfAdditionalTemplate,
  },
};

const Form = withTheme(Theme);

interface TailwindRJSFThemeProps {
  schema: RJSFSchema;
  uiSchema?: UiSchema;
  formData?: any;
  onSubmit: () => void
  onChange: (data: IChangeEvent, id: string | undefined) => void;
}

const TailwindRJSFTheme: React.FC<TailwindRJSFThemeProps> = ({schema, uiSchema, formData, onSubmit, onChange}) => {

  const handleBlur = (id: string, value: any) => {
    const fieldSchema = schema.properties?.[id];
    if (fieldSchema) {
      const result = validator.default.validateFormData(
        {[id]: value},
        {type: 'object', properties: {[id]: fieldSchema}}
      );
    }
  };

  return (
    <Form
      schema={schema}
      uiSchema={{
        ...uiSchema,
        'ui:field': 'root',
        'ui:ObjectFieldTemplate': ObjectFieldTemplate,
        'ui:FieldTemplate': FieldTemplate,
        'ui:onBlur': handleBlur,
      }}
      formData={formData}
      onChange={onChange}
      onSubmit={onSubmit}
      validator={validator as any}
    />
  );
};

export default TailwindRJSFTheme;