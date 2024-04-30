'use server'

import {OpenAPI, UsageService, UsageSummary} from "@eidolon/usage-client";

export async function usageForSession(sub: string): Promise<UsageSummary | null> {
  // eslint-disable-next-line no-undef
  OpenAPI.BASE = process.env.EIDOLON_USAGE_SERVER || "http://localhost:8527"
  return UsageService.getUsageSummarySubjectsSubjectIdGet({subjectId: sub}).catch((e: any) => {
    if (!process.env.EIDOLON_USAGE_SERVER) {
      console.info("Usage server is not available")
    } else if ('cause' in e && e.cause.code === "ECONNREFUSED") {
      console.error("Usage server is not available:", process.env.EIDOLON_USAGE_SERVER)
    } else {
      console.error(e)
    }
    return null
  })
}
