import {describe, expect, test} from "@jest/globals";
import {EidolonClient} from "../src/client";
import autoSetupPolly from "./polly_helper";

describe('eidolon-client', () => {
  autoSetupPolly();

  describe('main', () => {
    test('getAgents returns correct values', async () => {
      const client = new EidolonClient("http://localhost:8080")
      const agents = await client.getAgents()
      expect(agents).toEqual([
        "ErrorProneCodeAgent",
        "ExampleAuto",
        "ExampleGeneric",
        "HelloWorld",
        "ImageAgent",
        "OpenAIAssistants",
        "SpeechAgent",
        "StateMachine",
        "StreamingTest",
        "TreeOfThoughts",
      ]);
    });

    test("getProcesses contains newly created processes", async () => {
      const client = new EidolonClient("http://localhost:8080")
      const initial_processes = await client.getProcesses()
      const {status: p1} = await client.createProcess("HelloWorld")
      const {status: p2} = await client.createProcess("HelloWorld")
      const {status: p3} = await client.createProcess("HelloWorld")
      const processes = await client.getProcesses(initial_processes.total, 100)
      const processesList = processes.processes.filter(p =>
        p.process_id === p1.process_id || p.process_id === p2.process_id || p.process_id === p3.process_id)
      expect(processes.total).toBeGreaterThanOrEqual(3)
      expect(processesList).toEqual([p1, p2, p3])
    });
  });

  describe('eidolon-client/agent', () => {
    test('programs returns correct values', async () => {
      const client = new EidolonClient("http://localhost:8080")
      const {process} = await client.createProcess("HelloWorld")
      const agent = process.agent("HelloWorld")
      const programs = await agent.programs()
      expect(programs).toEqual([
        "return_string",
        "return_complex_object",
        "execute",
        "describe_images",
        "describe_image",
      ]);
    })
  });

  describe('eidolon-client/process', () => {
    test('status returns correct values', async () => {
      const client = new EidolonClient("http://localhost:8080")
      const {status: p1} = await client.createProcess("HelloWorld")
      const process = client.process(p1.process_id)
      const status = await process.status()
      expect(status).toEqual(p1)
    })

    test('delete deletes processes', async () => {
      const client = new EidolonClient("http://localhost:8080")
      const {status: p1} = await client.createProcess("HelloWorld")
      const process = client.process(p1.process_id)
      expect(await process.status()).toEqual(p1)
      await process.delete()
      const processes = await client.getProcesses()
      expect(processes.processes).not.toContain(p1)
    })

    test("action returns correct values", async () => {
      const client = new EidolonClient("http://localhost:8080")
      const {process: p1} = await client.createProcess("HelloWorld")
      const process = client.process(p1.process_id)
      const agent = process.agent("HelloWorld")
      const result = await agent.action("execute", {name: "World"})
      expect(result.data).toEqual({"welcome_message": "Hello, World World!"})
    })

    test("stream_action returns correct values", async () => {
      const client = new EidolonClient("http://localhost:8080")
      const {process: p1} = await client.createProcess("StreamingTest")
      const process = client.process(p1.process_id)
      const agent = process.agent("StreamingTest")
      const result = agent.stream_action("streaming", {name: "World"})
      const events = []
      for await (const data of result) {
        events.push(data)
      }
      const expectedEvents = [
        {
          stream_context: null,
          category: 'input',
          event_type: 'user_input',
          input: {name: 'World'}
        },
        {
          stream_context: null,
          category: 'start',
          event_type: 'agent_call',
          machine: 'http://localhost:8080',
          agent_name: 'StreamingTest',
          call_name: 'streaming',
          process_id: p1.process_id
        },
        {
          stream_context: null,
          category: 'output',
          event_type: 'string',
          content: 'Hello,'
        },
        {
          stream_context: null,
          category: 'output',
          event_type: 'string',
          content: 'World'
        },
        {
          stream_context: null,
          category: 'output',
          event_type: 'string',
          content: '!'
        },
        {
          stream_context: null,
          category: 'transform',
          event_type: 'agent_state',
          state: 'terminated',
          available_actions: []
        },
        {stream_context: null, category: 'end', event_type: 'success'}
      ]

      expect(events).toEqual(expectedEvents)
    })

    test("events returns correct values", async () => {
      const client = new EidolonClient("http://localhost:8080")
      const {process: p1} = await client.createProcess("StreamingTest")
      const process = client.process(p1.process_id)
      const agent = process.agent("StreamingTest")
      await agent.action("streaming", {name: "World"})
      const expectedEvents = [
        {
          category: 'input',
          event_type: 'user_input',
          input: {name: 'World'}
        },
        {
          category: 'start',
          event_type: 'agent_call',
          machine: 'http://localhost:8080',
          agent_name: 'StreamingTest',
          call_name: 'streaming',
          process_id: p1.process_id
        },
        {
          category: 'output',
          event_type: 'string',
          content: 'Hello,World!'
        },
        {
          category: 'transform',
          event_type: 'agent_state',
          state: 'terminated',
          available_actions: []
        },
        {category: 'end', event_type: 'success'}
      ]

      expect(await process.events()).toEqual(expectedEvents)
    })
  })
})
