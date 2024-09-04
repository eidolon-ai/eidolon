'use client'
import posthog from 'posthog-js'
import {PostHogProvider} from 'posthog-js/react'

const POSTHOG_KEY = "phc_9lcmDyxVkji98ggIqy2XvyVcItnrgdrMQhZBFp6Du5d"
const POSTHOG_HOST = "https://us.i.posthog.com"

if (typeof window !== 'undefined' && POSTHOG_KEY) {
  posthog.init(POSTHOG_KEY, {
    api_host: POSTHOG_HOST
  })

  const realFetch = globalThis.fetch;

  globalThis.fetch = function patchedFetch(uri, options) {
    if (!options) {
      options = {};
    }

    if (posthog) {
      options.headers = {...options.headers, 'X-Eidolon-Context': 'X-Posthog-Distinct-Id', 'X-Posthog-Distinct-Id': posthog.get_distinct_id()};
    }

    return realFetch(uri, options);
  };
}

export function PHProvider({
                             children,
                           }: {
  children: React.ReactNode
}) {
  return <PostHogProvider client={posthog} options={{disable_session_recording: true}}>{children}</PostHogProvider>
}
