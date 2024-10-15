import React from 'react';
import { ChevronDown } from 'lucide-react';

interface StyledSelectProps {
  options: string[];
  value: string;
  onChange: (value: string) => void;
  className?: string;
  size?: 'sm' | 'md' | 'lg'
}

const StyledSelect: React.FC<StyledSelectProps> = ({ options, value, onChange, className = '' , size = 'md'}) => {
  let classes: string
  switch (size) {
    case 'sm':
      classes = 'text-xs py-1.5 pl-1.5 pr-7 leading-3 '
      break;
    case 'md':
      classes = 'text-sm py-2 pl-3 pr-10 leading-5 '
      break;
    case 'lg':
      classes = 'text-base py-2 pl-3 pr-10 leading-5 '
      break;
  }
  return (
    <div className={`relative ${className}`}>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className={`appearance-none w-full bg-white border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 ${classes}`}
      >
        {options.map((option) => (
          <option key={option} value={option}>
            {option}
          </option>
        ))}
      </select>
      <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
        <ChevronDown className="h-4 w-4" />
      </div>
    </div>
  );
};

export default StyledSelect;