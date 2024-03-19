import { useRouter } from 'next/navigation';
import { useCallback } from 'react';

/**
 * Hook to navigate using router from next/router
 * @returns {function} call this function(url: string, replacePass = false) to navigate to the specified url
 */
export function useNavigate() {
  const router = useRouter();

  return useCallback(
    (url: string, replacePath = false) => (replacePath ? router.replace(url) : router.push(url)),
    [router]
  );
}
