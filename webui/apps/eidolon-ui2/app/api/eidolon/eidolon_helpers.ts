import {ProcessesHandler, ProcessEventsHandler, ProcessHandler} from "@eidolon/components";
import {auth} from "../../../auth";

const getAccessToken = async () => {
  const session = await auth()
  return session?.user?.access_token
}

export const _processesHandler= new ProcessesHandler(getAccessToken)
export const _processHandler= new ProcessHandler(getAccessToken)
export const _processEventHandler= new ProcessEventsHandler(getAccessToken)

export const processesHandler= {
  GET: _processesHandler.GET.bind(_processesHandler),
  POST: _processesHandler.POST.bind(_processesHandler)
}

export const processHandler= {
  GET: _processHandler.GET.bind(_processHandler),
  DELETE: _processHandler.DELETE.bind(_processHandler)
}

export const processEventHandler= {
  GET: _processEventHandler.GET.bind(_processEventHandler),
  POST: _processEventHandler.POST.bind(_processEventHandler),
}
