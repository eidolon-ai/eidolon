import {describe, expect, test} from "@jest/globals"
import {ProcessesHandler} from "../../src/server/processes-server-handler"
import autoSetupPolly from "../polly_helper"
import {getProcessStatus, getRootProcesses} from "../../src/client-api-helpers/process-helper";
import {HttpException} from "@eidolon/client";
import {fail} from "node:assert";

const processesHandler = new ProcessesHandler(async () => '')

describe('process client helper', () => {
  autoSetupPolly()

  const oldFetch = global.fetch
  global.fetch = (url, ...rest) => {
    url = "http://localhost:3000" + url
    return oldFetch(url, ...rest)
  }

  describe('getRootProcesses', () => {
    test('returns single process from today', async () => {
      const processes = await getRootProcesses('http://localhost:8080')
      expect(processes).toEqual([
        {
          "agent": "conversational_agent",
          "available_actions": [
            "converse",
            "generate_title"
          ],
          "created": "2024-04-22T11:15:34.241671",
          "id": "66267f160c3a347cff5dc9db",
          "machine": "http://localhost:8080",
          "parent_process_id": null,
          "path": "/chat/66267f160c3a347cff5dc9db",
          "process_id": "66267f160c3a347cff5dc9db",
          "state": "initialized",
          "title": "title",
          "updated": "2024-04-22T11:15:34.241671"
        }
      ])
    })

    test("returns 404 if eidolon server is down", async () => {
      try {
        await getRootProcesses('http://localhost:8080')
        fail('should have thrown')
      } catch (e) {
        expect(e.status).toBe(404)
      }
    })
  })

  describe('getProcessStatus', () => {
    test('returns process', async () => {
      const process = await getProcessStatus('http://localhost:8080', "66267f160c3a347cff5dc9db")
      expect(process).toEqual(
        {
          "agent": "conversational_agent",
          "available_actions": [
            "converse",
            "generate_title"
          ],
          "created": "2024-04-22T11:15:34.241671",
          "machine": "http://localhost:8080",
          "parent_process_id": null,
          "process_id": "66267f160c3a347cff5dc9db",
          "state": "initialized",
          "title": "title",
          "updated": "2024-04-22T11:15:34.241671"
        }
      )
    })

    test("returns 404 if eidolon server is down", async () => {
      try {
        await getProcessStatus('http://localhost:8080', "66267f160c3a347cff5dc9db")
      } catch (e) {
        expect(e.status).toBe(404)
        return
      }
      fail('should have thrown')
    })
  })
})
