import {ServerHandler} from "@eidolon/components";
import {getSession} from "next-auth/react";
import ProcessEventsHandler = ServerHandler.ProcessEventsHandler;


const getAccessToken = async () => {
  const session = await getSession()
  return session?.user?.access_token
}

const processHandler = new ProcessEventsHandler(getAccessToken)
export {processHandler as GET, processHandler as POST}
