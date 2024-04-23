import {createMocks} from 'node-mocks-http'
import {describe, expect, test} from "@jest/globals"
import {ProcessesHandler, ProcessHandler} from "../../src/server/processes-server-handler"
import autoSetupPolly from "../polly_helper"

const processesHandler = new ProcessesHandler(async () => '')
const processHandler = new ProcessHandler(async () => '')

describe('server-handler', () => {
  autoSetupPolly()

  describe('ProcessesHandler', () => {
    test('GET returns process list', async () => {
      // const process = await processesHandler.createProcess('http://localhost:8080', 'conversational_agent', 'title')
      const {req} = createMocks({
        method: 'GET',
        url: 'http://localhost/processes?machineURL=http://localhost:8080'
      })
      // @ts-ignore
      const response = await processesHandler.GET(req)
      expect(response.status).toBe(200)
      const json = await response.json()
      expect(json).toEqual(
        {
          "next": "http://localhost:8080/processes?skip=0&limit=100/processes/?limit=100&skip=100",
          "processes": [
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
          ],
          "total": 1
        }
      )
    })
    test('GET returns 422 if machineURL is missing', async () => {
      const {req} = createMocks({
        method: 'GET',
        url: 'http://localhost/processes'
      })
      // @ts-ignore
      const response = await processesHandler.GET(req)
      expect(response.status).toBe(422)
    })

    test('GET returns 404 if server is down', async () => {
      const {req} = createMocks({
        method: 'GET',
        url: 'http://localhost/processes?machineURL=http://localhost:8080'
      })
      // @ts-ignore
      const response = await processesHandler.GET(req)
      expect(response.status).toBe(404)
    })

    test('GET returns error when auth fails', async () => {
      const {req} = createMocks({
        method: 'GET',
        url: 'http://localhost/processes?machineURL=http://localhost:8080'
      })
      // @ts-ignore
      const response = await processesHandler.GET(req)
      expect(response.status).toBe(401)
    })
  })

  describe('ProcessHandler', () => {
    test('GET returns process', async () => {
      // const process = await processesHandler.createProcess('http://localhost:8080', 'conversational_agent', 'title')
      const {req} = createMocks({
        method: 'GET',
        url: 'http://localhost/process/66267f160c3a347cff5dc9db?machineURL=http://localhost:8080'
      })
      // @ts-ignore
      const response = await processHandler.GET(req, {params: {processid: '66267f160c3a347cff5dc9db'}})
      expect(response.status).toBe(200)
      const json = await response.json()
      expect(json).toEqual(
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
    test('GET returns 422 if machineURL is missing', async () => {
      const {req} = createMocks({
        method: 'GET',
        url: 'http://localhost/processes'
      })
      // @ts-ignore
      const response = await processHandler.GET(req, {params: {processid: '66267f160c3a347cff5dc9db'}})
      expect(response.status).toBe(422)
    })

    test('GET returns 404 if server is down', async () => {
      const {req} = createMocks({
        method: 'GET',
        url: 'http://localhost/processes?machineURL=http://localhost:8080'
      })
      // @ts-ignore
      const response = await processHandler.GET(req, {params: {processid: '66267f160c3a347cff5dc9db'}})
      expect(response.status).toBe(404)
    })

    test('GET returns error when auth fails', async () => {
      const {req} = createMocks({
        method: 'GET',
        url: 'http://localhost/processes?machineURL=http://localhost:8080'
      })
      // @ts-ignore
      const response = await processHandler.GET(req, {params: {processid: '66267f160c3a347cff5dc9db'}})
      expect(response.status).toBe(401)
    })
  })
})
