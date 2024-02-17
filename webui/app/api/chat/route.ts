'use server'

import {revalidateTag} from 'next/cache'

import {type Chat, ProcessState} from '@/lib/types'
import {getServerSession} from "next-auth";
import {authOptions} from "@/app/api/auth/[...nextauth]/route";
import {DateTime, Interval} from "luxon";

const getUserId = (async () => (await getServerSession(authOptions))?.user?.id)

const chatServerURL = process.env.EIDOLON_SERVER

type testTuple = [boolean, string]

const groups = [
  (date: DateTime): testTuple => {
    return [Interval.fromDateTimes(DateTime.now().startOf('day'), DateTime.now()).contains(date), "Today"]
  },
  (date: DateTime): testTuple => {
    return [Interval.fromDateTimes(DateTime.now().startOf('day').minus({day: 1}), DateTime.now()).contains(date), "Yesterday"]
  },
  (date: DateTime): testTuple => {
    return [Interval.fromDateTimes(DateTime.now().startOf('week'), DateTime.now()).contains(date), "This week"]
  },
  (date: DateTime): testTuple => {
    return [Interval.fromDateTimes(DateTime.now().startOf('week').minus({month: 1}), DateTime.now()).contains(date), "Last week"]
  },
  // this month
  (date: DateTime): testTuple => {
    return [Interval.fromDateTimes(DateTime.now().startOf('month'), DateTime.now()).contains(date), date.toFormat(
      'LLLL')]
  },
  // -1 month
  (date: DateTime): testTuple => {
    return [Interval.fromDateTimes(DateTime.now().startOf('month').minus({month: 1}), DateTime.now())
      .contains(date), date.toFormat('LLLL')]
  },
  // -2 month
  (date: DateTime): testTuple => {
    return [Interval.fromDateTimes(DateTime.now().startOf('month').minus({month: 2}), DateTime.now())
      .contains(date), date.toFormat('LLLL')]
  },
  // -3 month
  (date: DateTime): testTuple => {
    return [Interval.fromDateTimes(DateTime.now().startOf('month').minus({month: 3}), DateTime.now())
      .contains(date), date.toFormat('LLLL')]
  },
  // -4 month
  (date: DateTime): testTuple => {
    return [Interval.fromDateTimes(DateTime.now().startOf('month').minus({month: 4}), DateTime.now())
      .contains(date), date.toFormat('LLLL')]
  },
  // -5 month
  (date: DateTime): testTuple => {
    return [Interval.fromDateTimes(DateTime.now().startOf('month').minus({month: 5}), DateTime.now())
      .contains(date), date.toFormat('LLLL')]
  },
  // older
  (_date: DateTime): testTuple => {
    return [true, "Older"]
  },
]
const groupChat = (item: Chat) => {
  let dateTime = DateTime.fromISO(item.updated);
  return groups.reduce((reducer, fn) => {
    const test = fn(dateTime)
    return (reducer.length || !test[0]) ? reducer : test[1]
  }, "")
}

export async function getChatsForUI() {
  let data = (await getChats()).sort((a, b) => {
    return DateTime.fromISO(b.updated).toMillis() - DateTime.fromISO(a.updated).toMillis()
  })
  data = Object.values(data.reduce((collector, item) => {
    if (!item.parent_process_id) {
      collector[item.process_id] = {...collector[item.process_id], ...item}
    } else {
      if (!collector[item.parent_process_id]) {
        collector[item.parent_process_id] = {
          agent: item.agent,
          id: item.parent_process_id,
          title: item.parent_process_id,
          state: "Draft",
          path: `/chat/${item.parent_process_id}`,
          userId: "1",
          created: item.created,
          updated: item.updated,
          process_id: item.parent_process_id,
          children: []
        }
      }
      if (!collector[item.parent_process_id].children) {
        collector[item.parent_process_id].children = []
      }
      collector[item.parent_process_id].children!.push(item)
    }
    return collector
  }, {} as Record<string, Chat>))

  return data.reduce((collector, item) => {
    const title = groupChat(item)
    if (!collector[title]) collector[title] = []
    collector[title].push(item)
    return collector
  }, {} as Record<string, Chat[]>)
}

export async function getChats(): Promise<Chat[]> {
  const userId = await getUserId()
  const results = await fetch(`${chatServerURL}/system/processes?userId=${userId}`,
    {next: {tags: ['chats']}}
  ).then(resp => resp.json())

  const ret = []
  for (const json of results) {
    json.id = json.process_id
    json.title = json.title || json.agent
    json.userId = userId
    json.path = `/chat/${json.id}`
    ret.push(json as Chat)
  }

  return ret
}

export async function createPID(agentName: string, title: string) {
  const userId = await getUserId()
  const body = {title: title}
  const results = await fetch(`${chatServerURL}/agents/${agentName}/processes`, {
    method: "POST",
    body: JSON.stringify(body),
    headers: {
      "Content-Type": "application/json"
    }
  })

  revalidateTag(`chats`)
  const json = await results.json()
  return json["process_id"]
}

export async function getPIDStatus(agentName: string, process_id: string) {
  const userId = await getUserId()
  return fetch(`${chatServerURL}/agents/${agentName}/processes/${process_id}/status?userId=${userId}`)
    .then(resp => {
      if (resp.status === 404) {
        return null
      } else if (resp.status !== 200) {
        return resp.text().then(text => {
          return {
            state: "http_error",
            error: text,
            available_actions: []
          } as ProcessState
        })
      }
      return resp.json().then((json: Record<string, any>) => json as ProcessState)
    })
}

export async function getChat(id: string) {
  const userId = await getUserId()
  if (!userId || !id) {
    return null
  }
  const json = await fetch(`${chatServerURL}/system/processes/${id}?userId=${userId}`).then(resp => resp.json())

  json.id = json.process_id
  json.title = json.title || json.agent
  json.userId = userId
  json.path = `/chat/${json.id}`

  return json as Chat
}

export async function deleteChat(agentName: string, process_id: string) {
  const userId = await getUserId()
  await fetch(`${chatServerURL}/agents/${agentName}/processes/${process_id}?userId=${userId}`, {
    method: "DELETE"
  })
}
