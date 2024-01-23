import json

from markdown_it import MarkdownIt
from markdown_it.rules_core import StateCore


class StreamProcessor:
    def __init__(self):
        self.available_actions = []
        self.process_id = None

    def _process_events(self, response):
        for event in response:
            if event.data:
                server_event = json.loads(event.data)
                if server_event["event_type"] == "string_output":
                    # Append the new content to the buffer
                    yield server_event["content"]
                elif server_event["event_type"] == "object_output":
                    yield json.dumps(server_event["content"])
                elif server_event["event_type"] == "agent_state":
                    self.available_actions = server_event["available_actions"]
                elif server_event["event_type"] == "start" and server_event["start_type"] == "agent_call":
                    self.process_id = server_event["process_id"]

    def generate_tokens(self, response):
        input = self._process_events(response)
        parser = MarkdownIt().enable("strikethrough").enable("table")
        # change this to enable the text to be a generator looking that the state of the last token in the stream and either adding to it or yielding a new token
        env = {}
        num_tokens_processed = 0
        new_line_encountered = True
        wait_for_new_line = False
        in_fence = False
        block_starts = ["*", "-", "#", "`", ">", "|", "[", "!", "_", "~", " "]

        def line_starts_with_block_start(line: str):
            return len(line) > 0 and ((line[0] in block_starts or line[0].isdigit()) and not in_fence
                                      or line[0] == "`" and in_fence)

        text = ""
        for chunk in input:
            lines = chunk.split("\n")
            extra_text = ""
            if len(lines) <= 1:
                text += chunk
                # we are waiting for a new line and didn't get it, just add the chunk and continue
                if wait_for_new_line:
                    continue
                elif new_line_encountered and line_starts_with_block_start(chunk):
                    wait_for_new_line = True
                    new_line_encountered = False
                    continue
            else:
                for line in lines[:-1]:
                    text += line + "\n"
                if line_starts_with_block_start(lines[-1]) and not chunk.endswith("\n"):
                    extra_text = lines[-1]
                    new_line_encountered = False
                    wait_for_new_line = True
                else:
                    text += lines[-1]
                    wait_for_new_line = False
                    new_line_encountered = chunk.endswith("\n")

            state = StateCore(text, parser, env)
            parser.core.process(state)
            # iterate over tokens in reverse order finding the last token with type "inline"
            end_token_pos = len(state.tokens)
            in_fence = False
            for i in range(len(state.tokens) - 1, -1, -1):
                if state.tokens[i].type == "inline":
                    # this might be a table so we can't process it yet
                    if not(state.tokens[i].content.startswith("|") and state.tokens[i-1].type == "paragraph_open"):
                        end_token_pos = i
                        break
                elif state.tokens[i].type == "fence":
                    in_fence = True
                    end_token_pos = i
                    break
            if len(state.tokens) > 0:
                for token in state.tokens[num_tokens_processed:end_token_pos]:
                    yield token
                num_tokens_processed = end_token_pos
            text += extra_text

        state = StateCore(text, parser, env)
        parser.core.process(state)
        for token in state.tokens[num_tokens_processed:]:
            yield token
