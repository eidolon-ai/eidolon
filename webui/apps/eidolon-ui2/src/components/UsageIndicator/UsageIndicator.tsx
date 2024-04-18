import {Box, LinearProgress, Typography} from "@mui/material";
import * as React from "react";
import {useEffect, useState} from "react";
import {UsageSummary} from "@eidolon/usage-client"
import {usageForSession} from "@eidolon/components";
import {useSession} from "next-auth/react";
import {useEidolonContext} from "@eidolon/components/src/provider/eidolon_provider";

export const revalidate=1

export function UsageIndicator({...restOfProps}) {
  const [usageData, setUsageData] = useState<UsageSummary | null>(null)
  const [eidolonContext] = useEidolonContext()

  const {data: session} = useSession()
  useEffect(() => {
    if (session?.user?.id) {
      usageForSession(session.user.id, eidolonContext.usageSeed).then((data) => {
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
