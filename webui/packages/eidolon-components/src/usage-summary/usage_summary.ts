'use server'

import {OpenAPI, UsageService, UsageSummary} from "@eidolon/usage-client";

export async function usageForSession(sub: string): Promise<UsageSummary | null> {
  // eslint-disable-next-line no-undef
  const usageServerLoc = process.env.EIDOLON_USAGE_SERVER;
  if (usageServerLoc) {
    OpenAPI.BASE = usageServerLoc
    return UsageService.getUsageSummarySubjectsSubjectIdGet({subjectId: sub})
  } else {
    return null
  }
}
