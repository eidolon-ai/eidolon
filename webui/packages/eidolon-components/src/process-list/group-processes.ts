import {ProcessStatus} from "../lib/types.js";
import {DateTime, Interval} from "luxon";

export const groupProcessesByUpdateDate = async (processes: ProcessStatus[]) => {
  return processes.reduce((collector, item) => {
    const title = groupChat(item)
    if (!collector[title]) collector[title] = []
    collector[title]!.push(item)
    return collector
  }, {} as Record<string, ProcessStatus[]>)
}

const groupChat = (item: ProcessStatus) => {
  let dateTime = DateTime.fromISO(item.updated);
  return groups.reduce((reducer, fn) => {
    const test = fn(dateTime)
    return (reducer.length || !test[0]) ? reducer : test[1]
  }, "")
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
