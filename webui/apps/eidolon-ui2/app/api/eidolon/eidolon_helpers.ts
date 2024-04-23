import {ProcessesHandler, ProcessEventsHandler, ProcessHandler} from "@eidolon/components";
import {auth} from "../../../auth";
import {AgentHandler, FileHandler, FilesHandler, MachineHandler} from "@eidolon/components/src/server/processes-server-handler";

const getAccessToken = async () => {
  const session = await auth()
  return session?.user?.access_token
}

export const _processesHandler= new ProcessesHandler(getAccessToken)
export const _processHandler= new ProcessHandler(getAccessToken)
export const _processEventHandler= new ProcessEventsHandler(getAccessToken)
export const _filesEventHandler= new FilesHandler(getAccessToken)
export const _fileEventHandler= new FileHandler(getAccessToken)
export const _machineHandler= new MachineHandler(getAccessToken)
export const _agentHandler= new AgentHandler(getAccessToken)

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

export const filesHandler= {
  POST: _filesEventHandler.POST.bind(_filesEventHandler),
}

export const fileHandler= {
  GET: _fileEventHandler.GET.bind(_fileEventHandler),
  POST: _fileEventHandler.POST.bind(_fileEventHandler),
  DELETE: _fileEventHandler.DELETE.bind(_fileEventHandler),
}

export const machineHandler= {
  GET: _machineHandler.GET.bind(_machineHandler),
}

export const agentHandler= {
  GET: _agentHandler.GET.bind(_agentHandler),
}
