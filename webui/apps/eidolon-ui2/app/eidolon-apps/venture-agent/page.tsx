import {Box, ListItem, ListItemText, ListSubheader, Typography} from "@mui/material";
import {getApp} from "@/utils/eidolon-apps";
import {CopilotParams} from "@eidolon/components";
import List from "@mui/material/List";
import ListItemWithCode from "./ListItemWithCode";

export interface HomePageProps {
}

const Page = () => {
  const app = getApp("venture-agent")!
  const params = app!.params as CopilotParams

  function showConfiguration() {

  }

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
          Venture Agent is a tool that helps you to create and manage your own venture thesis.
          Start by searching for companies you are interested in and add them to your portfolio.
          Once you've added a company, you can research it further.
        </Typography>
        <br/>

        <Typography variant={"h5"}>Composition</Typography>
        <List>
          <ListSubheader>
            <Typography variant={"body1"}>
              The venture super-agent is a collection of four agents, venture_copilot, speech_agent, CompanyFinder, and CompanyResearcher
            </Typography>
          </ListSubheader>
          <ListItemWithCode
            title={"venture_copilot"}
            text={"This is the main controller for the super-agent. Its main responsibility is to store information for the UI and to kick off the initial operations for CompanyFinder and CompanyResearcher."}
            configFile={"https://raw.githubusercontent.com/eidolon-ai/eidolon/main/examples/eidolon_examples/venture_search_agent/resources/venture_copilot.yaml"}
            configFileExternalLink={"https://github.com/eidolon-ai/eidolon/blob/main/examples/eidolon_examples/venture_search_agent/resources/venture_copilot.yaml"}
            codeFile={"https://raw.githubusercontent.com/eidolon-ai/eidolon/main/examples/eidolon_examples/venture_search_agent/venture_copilot.py"}
            codeFileExternalLink={"https://github.com/eidolon-ai/eidolon/blob/main/examples/eidolon_examples/venture_search_agent/venture_copilot.py"}
          />
          <ListItemWithCode
            title={"CompanyFinder"}
            text={"This agent is used find companies to research. I has a search tool and a browser tool enabled."}
            configFile={"https://raw.githubusercontent.com/eidolon-ai/eidolon/main/examples/eidolon_examples/venture_search_agent/resources/CompanyFinder.yaml"}
            configFileExternalLink={"https://github.com/eidolon-ai/eidolon/blob/examples/eidolon_examples/venture_search_agent/resources/CompanyFinder.yaml"}
            builtinAgentType={"SimpleAgent"}
            codeFileExternalLink={"https://github.com/eidolon-ai/eidolon/blob/main/sdk/eidolon_ai_sdk/agent/simple_agent.py"}
          />
          <ListItemWithCode
            title={"CompanyResearcher"}
            text={"This agent is used to research an individual company. I has a search tool, a browser tool, and the API tool configured to enhance the data using Harmonic's API."}
            configFile={"https://raw.githubusercontent.com/eidolon-ai/eidolon/main/examples/eidolon_examples/venture_search_agent/resources/CompanyResearcher.yaml"}
            configFileExternalLink={"https://github.com/eidolon-ai/eidolon/blob/examples/eidolon_examples/venture_search_agent/resources/CompanyResearcher.yaml"}
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
              ● Code Agent
            </ListItemText>
          </ListItem>
          <ListItem>
            <ListItemText>
              ● Chatbot Agent
            </ListItemText>
          </ListItem>
          <ListItem>
            <ListItemText>
              ● Search LogicUnit
            </ListItemText>
          </ListItem>
          <ListItem>
            <ListItemText>
              ● Browser LogicUnit:
            </ListItemText>
          </ListItem>
          <ListItem>
            <ListItemText>
              ● API LogicUnit
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
