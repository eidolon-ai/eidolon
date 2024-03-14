import {ServerHandler} from "@eidolon/components";
import {NextRequest, NextResponse} from "next/server";
import {getSession} from "next-auth/react";
import ProcessHandler = ServerHandler.ProcessHandler;


const getAccessToken = async () => {
  const session = await getSession()
  return session?.user?.access_token
}

const processHandler = new ProcessHandler(getAccessToken)
export {processHandler as GET, processHandler as POST, processHandler as DELETE}
