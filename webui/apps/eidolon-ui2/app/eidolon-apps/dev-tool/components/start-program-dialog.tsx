'use client'

import { useEffect, useRef } from 'react';
import { usePathname, useRouter } from 'next/navigation';
import { X } from 'lucide-react';
import { ChooseAgentForm, getAppPathFromPath } from '@eidolon-ai/components/client';

interface StartProgramDialogProps {
  machineUrl: string;
  open: boolean;
  defaultAgent?: string;
  onClose: (wasCanceled: boolean) => void;
}

export function StartProgramDialog({ open, onClose, machineUrl, defaultAgent }: StartProgramDialogProps) {
  const router = useRouter();
  const pathname = usePathname();
  const dialogRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleEscape = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        onClose(true);
      }
    };

    if (open) {
      document.addEventListener('keydown', handleEscape);
      return () => {
        document.removeEventListener('keydown', handleEscape);
      };
    }
  }, [open, onClose]);

  const handleCancel = () => {
    onClose(true);
  };

  const handleSubmit = (processId: string) => {
    const appPath = getAppPathFromPath(pathname);
    if (appPath) {
      router.push(`${appPath}/${processId}`);
      onClose(false);
    }
  };

  if (!open) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div
        ref={dialogRef}
        className="bg-white rounded-lg shadow-xl w-full max-w-2xl mx-4 overflow-hidden"
        role="dialog"
        aria-modal="true"
      >
        <div className="p-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold">Start a new chat</h2>
            <button onClick={handleCancel} className="text-gray-500 hover:text-gray-700">
              <X className="h-6 w-6" />
            </button>
          </div>
          <p className="text-sm text-gray-500 mb-4">Choose the agent and then click Start.</p>
          <div className="border-t border-gray-200 my-4"></div>
          <div className="py-4">
            <ChooseAgentForm
              machineUrl={machineUrl}
              handleSubmit={handleSubmit}
              defaultAgent={defaultAgent}
            />
          </div>
          <div className="flex justify-end space-x-4 mt-6">
            <button
              onClick={handleCancel}
              className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Cancel
            </button>
            <button
              form="start-program-form"
              type="submit"
              className="px-4 py-2 bg-indigo-600 border border-transparent rounded-md text-sm font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Start
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}