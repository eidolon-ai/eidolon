'use server'

import {OpenAPI, UsageService, UsageSummary} from "@eidolon/usage-client";

let usageSummaryCache: UsageSummary | null = null
let usageCacheSeed = -1

export async function usageForSession(sub: string, seed: number) {
  // eslint-disable-next-line no-unused-vars
  OpenAPI.BASE = process.env.EIDOLON_USAGE_SERVER || "http://localhost:8527"
  if (seed != usageCacheSeed) {
    if (!usageSummaryCache) {
      usageSummaryCache = await UsageService.getUsageSummarySubjectsSubjectIdGet({subjectId: sub})
    }
    usageCacheSeed = seed
  }
  return usageSummaryCache
}

export async function clearUsageCache() {
  usageSummaryCache = null
}
