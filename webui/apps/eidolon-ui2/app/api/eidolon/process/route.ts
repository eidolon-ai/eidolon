import {ServerHandler} from "@eidolon/components";
import {getSession} from "next-auth/react";
import ProcessesHandler = ServerHandler.ProcessesHandler;

const getAccessToken = async () => {
  const session = await getSession()
  return session?.user?.access_token
}

const processHandler = new ProcessesHandler(getAccessToken)
export {processHandler as GET}
