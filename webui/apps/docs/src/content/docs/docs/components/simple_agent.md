---
title: SimpleAgentSpec
description: Component - SimpleAgentSpec
---
The `SimpleAgentSpec` class defines the basic configuration for a SimpleAgent within the Eidolon framework. This agent is designed to be a flexible, modular component that can interact with various processing units and perform a range of actions based on its configuration.


## Defining Actions
The simple agent has a constant system prompt, and any number of dynamic actions that can will be templated via jinja2.
Arguments used in an actions user prompt will be automatically added to the rest endpoints openapi schema. For example,
`write me a poem about {{ topic }} in the voice of {{ actor }}` will create an action that requires a topic and actor as 
json in the body of the http request. "**body**" is a reserved keyword, and if it is used by itself, the request will accept 
text/plain in the body of the request (which will then template `{{ body }}`).

Note that multiple actions can be added on the agent. Each can define different allowed states and output state, 
allowing for a powerful state machine to be built without needing to define a custom agent template.


## Spec

| Key                  | Description                                                                                                                                                                                    |
|----------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| description          | `type`: Optional[str]<br/>`Default`: None<br/>`Description:` Provides a brief description of the agent's purpose or role within the system.                                                    |
| system_prompt        | `type`: str<br/>`Default`: "You are a helpful assistant"<br/>`Description:` Sets the default communication prompt for the agent, guiding its conversational context.                           |
| agent_refs           | `type`: List[str]<br/>`Default`: []<br/>`Description:` References to other agents or components that this agent might interact with or depend on.                                              |
| actions              | `type`: List[ActionDefinition]<br/>`Default`: [ActionDefinition()]<br/>`Description:` Defines the actions this agent can perform, each specified by an ActionDefinition.                       |
| apu                  | `type`: Reference[APU]<br/>`Default`: None<br/>`Description:` Optionally specifies a primary Agent Processing Unit (APU) for processing requests.                                              |
| apus                 | `type`: List[NamedCPU]<br/>`Default`: []<br/>`Description:` Lists additional APUs that the agent can utilize, providing flexibility in processing capabilities.                                |
| title_generation_mode| `type`: Literal["none", "on_request"]<br/>`Default`: "on_request"<br/>`Description:` Determines how the agent generates titles for its processes, either dynamically on request or not at all. |
| doc_processor        | `type`: Reference[DocumentProcessor]<br/>`Default`: Reference[DocumentProcessor]<br/>`Description:` Manages document-related tasks within the agent's operational scope.                       |

### ActionDefinition Spec

| Key                   | Description                                                                                                                                                                                                   |
|-----------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| name                  | `type`: str<br/>`Default`: "converse"<br/>`Description:` The name of the action.                                                                                                                             |
| title                 | `type`: Optional[str]<br/>`Default`: None<br/>`Description:` The title of the action, used for display or descriptive purposes.                                                                                                      |
| sub_title             | `type`: Optional[str]<br/>`Default`: None<br/>`Description:` A subtitle for the action, providing additional context or information.                                                                                                 |
| description           | `type`: Optional[str]<br/>`Default`: None<br/>`Description:` A description of what the action does or is used for.                                                                                                                  |
| user_prompt           | `type`: str<br/>`Default`: "{{ body }}"<br/>`Description:` The prompt presented to the user, which can include placeholders for dynamic content.                                                                                    |
| input_schema          | `type`: Dict[str, dict]<br/>`Default`: {}<br/>`Description:` Defines the structure of the input data expected by the action.                                                                                                        |
| output_schema         | `type`: Union[Literal["str"], Dict[str, Any]]<br/>`Default`: "str"<br/>`Description:` Specifies the format of the output data from the action. Can be a simple string or a structured dictionary.                                    |
| allow_file_upload     | `type`: bool<br/>`Default`: False<br/>`Description:` Indicates whether file uploads are allowed as part of the action input.                                                                                                        |
| supported_mime_types  | `type`: List[str]<br/>`Default`: [] (supports all types)<br/>`Description:` List of MIME types supported for file uploads. An empty list means all types are supported.                                                             |
| allowed_states        | `type`: List[str]<br/>`Default`: ["initialized", "idle", "http_error"]<br/>`Description:` Specifies the states in which this action can be executed.                                                                               |
| output_state          | `type`: str<br/>`Default`: "idle"<br/>`Description:` The state of the system after the action has been executed.                                                                                                                    |


