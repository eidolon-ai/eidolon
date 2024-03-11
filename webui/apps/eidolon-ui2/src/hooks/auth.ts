import { useCallback } from 'react';
import { sessionStorageGet, sessionStorageDelete } from '@/utils/sessionStorage';
import { useAppStore } from '../store';

/**
 * Hook to detect is current user authenticated or not
 * @returns {boolean} true if user is authenticated, false otherwise
 */
export function useIsAuthenticated() {
  const [state] = useAppStore();
  let result = state.isAuthenticated;

  // TODO: AUTH: replace next line with access token verification
  result = Boolean(sessionStorageGet('access_token', ''));

  return result;
}

/**
 * Returns event handler to Logout current user
 * @returns {function} calling this event logs out current user
 */
export function useEventLogout() {
  const [, dispatch] = useAppStore();

  return useCallback(() => {
    // TODO: AUTH: replace next line with access token saving
    sessionStorageDelete('access_token');

    dispatch({ type: 'LOG_OUT' });
  }, [dispatch]);
}
