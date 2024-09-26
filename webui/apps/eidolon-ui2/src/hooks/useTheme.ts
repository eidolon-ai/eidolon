import { useEffect } from 'react';
import { useAppStore } from '../store/index';

export function useTheme() {
  const [state, dispatch] = useAppStore();

  useEffect(() => {
    const isDarkMode =
      state.themeMode === 'dark' ||
      (state.themeMode === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches);

    document.documentElement.classList.toggle('dark', isDarkMode);
  }, [state.themeMode]);

  const setTheme = (theme: 'light' | 'dark' | 'system') => {
    dispatch({
      type: 'DARK_MODE',
      payload: theme,
    });
  };

  return { theme: state.themeMode, setTheme };
}