import {ProcessesHandler, ProcessEventsHandler, ProcessHandler} from "@eidolon/components";
import {auth} from "../../../auth";

const getAccessToken = async () => {
  const session = await auth()
  return session?.user?.access_token
}

const _processesHandler= new ProcessesHandler(getAccessToken)
const _processHandler= new ProcessHandler(getAccessToken)
const _processEventHandler= new ProcessEventsHandler(getAccessToken)

export const processesHandler= {
  GET: _processesHandler.GET.bind(_processesHandler)
}
export const processHandler= {
  GET: _processHandler.GET.bind(_processHandler),
  POST: _processHandler.POST.bind(_processHandler),
  DELETE: _processHandler.DELETE.bind(_processHandler)
}

export const processEventHandler= {
  GET: _processEventHandler.GET.bind(_processEventHandler),
  POST: _processEventHandler.POST.bind(_processEventHandler),
}
