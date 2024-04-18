'use server'

import {OpenAPI, UsageService, UsageSummary} from "@eidolon/usage-client";
import {revalidatePath} from "next/cache";

OpenAPI.BASE = process.env.EIDOLON_USAGE_SERVER || "http://localhost:8527"

let usageSummaryCache: UsageSummary | null = null
let usageCacheSeed = -1

export async function usageForSession(sub: string, seed: number) {
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
