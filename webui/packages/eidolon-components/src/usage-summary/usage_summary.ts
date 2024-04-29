'use server'

import {OpenAPI, UsageService} from "@eidolon/usage-client";

export function usageForSession(sub: string) {
  // eslint-disable-next-line no-undef
  const usageServerLoc = process.env.EIDOLON_USAGE_SERVER;
  if (usageServerLoc) {
    OpenAPI.BASE = usageServerLoc
    return UsageService.getUsageSummarySubjectsSubjectIdGet({subjectId: sub})
  } else {
    return Promise.resolve(null)
  }
}
