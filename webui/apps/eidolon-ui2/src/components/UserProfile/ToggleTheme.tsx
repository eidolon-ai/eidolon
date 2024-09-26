import React from 'react';
import { Sun, Moon, Laptop } from 'lucide-react';
import {useTheme} from "../../hooks/useTheme.ts";

export function ToggleTheme() {
  const { theme, setTheme } = useTheme();

  const themes = [
    { value: 'light', icon: Sun, label: 'Light' },
    { value: 'system', icon: Laptop, label: 'System' },
    { value: 'dark', icon: Moon, label: 'Dark' },
  ];

  return (
    <div className="space-y-2">
      <h3 className="text-sm font-medium leading-none">Theme</h3>
      <div className="flex space-x-1">
        {themes.map(({ value, icon: Icon, label }) => (
          <button
            key={value}
            onClick={() => setTheme(value as 'light' | 'dark' | 'system')}
            className={`p-2 rounded-md transition-colors ${
              theme === value
                ? 'bg-primary text-primary-foreground'
                : 'bg-secondary text-secondary-foreground hover:bg-secondary/80'
            }`}
            aria-label={`${label} theme`}
          >
            <Icon className="h-4 w-4" />
            <span className="sr-only">{label}</span>
          </button>
        ))}
      </div>
    </div>
  );
}