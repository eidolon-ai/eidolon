import {Box, LinearProgress, Typography} from "@mui/material";
import * as React from "react";
import {useEffect, useState} from "react";
import {OpenAPI, UsageService, UsageSummary} from "@eidolon/usage-client"
import {useSession} from "next-auth/react";
import {useEidolonContext} from "@eidolon/components/client";

export const revalidate=1

export async function usageForSession(sub: string): Promise<UsageSummary | null> {
  // eslint-disable-next-line no-undef
  const envUsageLoc = process.env.EIDOLON_USAGE_SERVER;
  OpenAPI.BASE = envUsageLoc || "http://localhost:8527"
  return UsageService.getUsageSummarySubjectsSubjectIdGet({subjectId: sub}).catch((e: any) => {
    if (!envUsageLoc) {
      console.info("Usage server is not available")
    } else if ('cause' in e && e.cause.code === "ECONNREFUSED") {
      console.error("Usage server is not available:", envUsageLoc)
    } else {
      console.error(e)
    }
    return null
  })
}

export function UsageIndicator({...restOfProps}) {
  const [usageData, setUsageData] = useState<UsageSummary | null>(null)
  const [eidolonContext] = useEidolonContext()

  const {data: session} = useSession()
  useEffect(() => {
    if (session?.user?.id) {
      usageForSession(session.user.id).then((data) => {
        setUsageData(data)
      })
    }
  }, [session, eidolonContext.usageSeed]);
  if (usageData) {
    return (
      <Box sx={{display: 'flex', width: '100%', flexDirection: 'column', alignItems: "end"}} {...restOfProps}>
        <Box sx={{width: '100%', mr: 1, pt: "23px"}}>
          <LinearProgress sx={{height: '4px'}} variant="determinate" value={usageData.used / usageData.allowed * 100}/>
        </Box>
        <Box sx={{minWidth: 35, textAlign: "right", paddingTop: '2px', mr: '9px'}}>
          <Typography variant="body2" color="text.secondary">{usageData.used} / {usageData.allowed} seconds used</Typography>
        </Box>
      </Box>
    )
  } else {
    return <></>
  }
}
