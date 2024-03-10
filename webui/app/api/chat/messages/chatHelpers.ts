'use server'

import {Chat, ChatEvent, ProcessState} from "@/lib/types";
import {getServerSession} from "next-auth";
import {revalidatePath, revalidateTag} from "next/cache";
import authOptions from "@/app/api/auth/[...nextauth]/authOptions";
import {DateTime, Interval} from "luxon";

const chatServerURL = process.env.EIDOLON_SERVER

const getUser = (async () => (await getServerSession(authOptions))?.user)

export const getAuthHeaders = async () : Promise<Record<string, string>> => {
    const user = await getUser()
    if (!user?.access_token) {
        return {} as Record<string, string>
    }
    return {
        "Authorization": `Bearer ${user?.access_token}`
    }
}

export async function getChatEvents(agentName: string, processId: string) {
    revalidatePath(`${chatServerURL}/agents/${agentName}/processes/${processId}/events`)
    const auth_headers = await getAuthHeaders()
    const results = await fetch(`${chatServerURL}/agents/${agentName}/processes/${processId}/events`,{headers: auth_headers})
        .then(resp => resp.json())

    const ret = []
    for (const json of results) {
        ret.push(json as ChatEvent)
    }

    return ret
}


export async function getChat(id: string) {
    const auth_headers = await getAuthHeaders()
    const user = await getUser()
    if (!user || !id) {
        return null
    }
    const json = await fetch(`${chatServerURL}/system/processes/${id}`,{headers: auth_headers}).then(resp => {
        if (resp.ok) {
            return resp.json()
        } else {
            console.log("error", resp)
            return undefined
        }
    })

    if (json) {
        json.id = json.process_id
        json.title = json.title || json.agent
        json.userId = user.id
        json.path = `/chat/${json.id}`
    }
    return json as Chat
}

export async function deleteChat(agentName: string, process_id: string) {
    const auth_headers = await getAuthHeaders()
    await fetch(`${chatServerURL}/agents/${agentName}/processes/${process_id}`, {
        method: "DELETE",
        headers: auth_headers
    })
}

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
    const auth_headers = await getAuthHeaders()
    const results = await fetch(`${chatServerURL}/system/processes`,
        {
            next: {tags: ['chats']},
            headers: auth_headers
        }
    ).then(resp => {
        if (resp.status === 401) {
            console.log('Unauthenticated! Status: 401');
            return [];
        } else if (!resp.ok) {
            throw new Error(`HTTP error! status: ${resp.status}`);
        }
        return resp.json();
    })

    const ret = []
    for (const json of results) {
        json.id = json.process_id
        json.title = json.title || json.agent
        json.path = `/chat/${json.id}`
        ret.push(json as Chat)
    }

    return ret
}

export async function createPID(agentName: string, title: string) {
    const auth_headers = await getAuthHeaders()
    const body = {title: title}
    const results = await fetch(`${chatServerURL}/agents/${agentName}/processes`, {
        method: "POST",
        body: JSON.stringify(body),
        headers: {
            "Content-Type": "application/json",
            ...auth_headers
        }
    })

    revalidateTag(`chats`)
    const json = await results.json()
    return json["process_id"]
}

export async function getPIDStatus(agentName: string, process_id: string) {
    const auth_headers = await getAuthHeaders()
    return fetch(`${chatServerURL}/agents/${agentName}/processes/${process_id}/status`,{headers: auth_headers})
        .then(resp => {
            if (resp.status === 404) {
                return null
            }
            return resp.json().then((json: Record<string, any>) => json as ProcessState)
        })
}
