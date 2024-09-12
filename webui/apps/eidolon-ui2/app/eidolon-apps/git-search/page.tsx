import {Box, ListItem, ListItemText, ListSubheader, Typography} from "@mui/material";
import {getApp} from "@/utils/eidolon-apps";
import List from "@mui/material/List";
import ListItemWithCode from "../../../components/ListItemWithCode";

const Page = () => {
  const app = getApp("git-search")!

  return (
    <Box component="main" sx={{
      flexGrow: 1, p: 3, alignItems: "start", height: "100%", display: 'flex', width: "100%",
      flexDirection: 'column',
      justifyContent: 'start',
    }}>
      <div style={{display: "relative", width: "100%"}}>
        <div style={{display: "fixed", "float": "right", margin: "8px"}}><img height={"128px"} width={"128px"} src={app.image} alt={app.name}/></div>
        <Typography variant={"h4"}>Venture Agent</Typography>
        <Typography variant={"body1"}>
          This agent allows you search a github repository's documentation and code using RAG. It uses the git_search agent in examples.
        </Typography>
        <br/>

        <Typography variant={"h5"}>Composition</Typography>
        <List>
          <ListSubheader>
            <Typography variant={"body1"}>
              The git search super-agent is a collection of three agents, repo_expert, repo_search, and speech-agent.
            </Typography>
          </ListSubheader>
          <ListItemWithCode
            title={"repo_expert"}
            text={"This is a copilot agent that is the fron-end to the search. It uses the repo_search agent to search docs and code. It supports uploading additional docs and will search across all files."}
            configFile={"https://raw.githubusercontent.com/eidolon-ai/eidolon/main/examples/eidolon_examples/git_search/repo_expert.yaml"}
            configFileExternalLink={"https://github.com/eidolon-ai/eidolon/blob/main/examples/eidolon_examples/git_search/repo_expert.yaml"}
            builtinAgentType={"SimpleAgent"}
            codeFileExternalLink={"https://github.com/eidolon-ai/eidolon/blob/main/sdk/eidolon_ai_sdk/agent/simple_agent.py"}
          />
          <ListItemWithCode
            title={"repo_search"}
            text={"This is the search agent. Its only responsibility is to index and search the files that match the given pattern in the git repository specified in the config file."}
            configFile={"https://raw.githubusercontent.com/eidolon-ai/eidolon/main/examples/eidolon_examples/git_search/repo_search.yaml"}
            configFileExternalLink={"https://github.com/eidolon-ai/eidolon/blob/examples/eidolon_examples/git_search/repo_search.yaml"}
            builtinAgentType={"SimpleAgent"}
            codeFileExternalLink={"https://github.com/eidolon-ai/eidolon/blob/main/sdk/eidolon_ai_sdk/agent/simple_agent.py"}
          />
        </List>
        <Typography variant={"h5"}>Eidolon features used</Typography>
        <List dense>
          <ListItem>
            <ListItemText>
              ● Multiple Agents
            </ListItemText>
          </ListItem>
          <ListItem>
            <ListItemText>
              ● Chatbot Agent
            </ListItemText>
          </ListItem>
          <ListItem>
            <ListItemText>
              ● DocumentManager
            </ListItemText>
          </ListItem>
          <ListItem>
            <ListItemText>
              ● Chatbot UI
            </ListItemText>
          </ListItem>
        </List>
      </div>
    </Box>
  )
    ;
}

export const revalidate = 0

export default Page;
