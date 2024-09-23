import React, { useRef, useEffect } from 'react';
import "./custom_text_area.css"

interface CustomTextareaProps {
  value: string;
  placeholder?: string;
  ariaLabel?: string;
  onChange: (value: string) => void;
  maxHeight?: string;
  handleEnter: () => void;
}

const CustomTextarea: React.FC<CustomTextareaProps> = ({
  value,
  placeholder = 'Type something...',
  ariaLabel = 'Editable text area',
  onChange,
  maxHeight = '18rem',
  handleEnter
}) => {
  const contentEditableRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const div = contentEditableRef.current;
    if (div && div.innerText !== value) {
      div.innerText = value;
    }
  }, [value]);

  const handleInput = () => {
    if (contentEditableRef.current) {
      const content = contentEditableRef.current.innerText;
      if (content !== value) {
        onChange(content);
      }
    }
  };

  const handleKeyDown = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleEnter();
    }
  };

  const handlePaste = (event: React.ClipboardEvent) => {
    event.preventDefault();
    const text = event.clipboardData.getData('text/plain');
    document.execCommand('insertText', false, text);
  };

  return (
    <div
      className="w-full overflow-y-auto break-words"
      style={{ maxHeight }}
      aria-label={ariaLabel}
    >
      <div
        ref={contentEditableRef}
        contentEditable="true"
        onKeyDown={handleKeyDown}
        onInput={handleInput}
        onPaste={handlePaste}
        translate="no"
        className="break-words max-w-[60ch] p-2 outline-none focus:outline-none"
        data-placeholder={placeholder}
      />
    </div>
  );
};

export default CustomTextarea;