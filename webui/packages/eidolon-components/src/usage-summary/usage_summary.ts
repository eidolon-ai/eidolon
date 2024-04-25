'use server'

import {OpenAPI, UsageService, UsageSummary} from "@eidolon/usage-client";

let usageSummaryCache: UsageSummary | null = null
let usageCacheSeed = -1

export async function usageForSession(sub: string, seed: number) {
  // eslint-disable-next-line no-undef
  const usageServerLoc = process.env.EIDOLON_USAGE_SERVER;
  if (usageServerLoc) {
    OpenAPI.BASE = usageServerLoc
    if (seed != usageCacheSeed) {
      if (!usageSummaryCache) {
        usageSummaryCache = await UsageService.getUsageSummarySubjectsSubjectIdGet({subjectId: sub})
      }
      usageCacheSeed = seed
    }
    return usageSummaryCache
  } else {
    return Promise.resolve(null)
  }
}

export async function clearUsageCache() {
  usageSummaryCache = null
}
