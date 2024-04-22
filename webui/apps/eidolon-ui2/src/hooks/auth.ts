import {useCallback} from 'react';
import {sessionStorageDelete} from '@/utils/sessionStorage';
import {useAppStore} from '../store';
import {useSession} from "next-auth/react";

/**
 * Hook to detect is current user authenticated or not
 * @returns {boolean} true if user is authenticated, false otherwise
 */
export function useIsAuthenticated(): boolean {
  const session = useSession();
  return !!session?.data;
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
