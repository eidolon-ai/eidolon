import {ToolCallElement} from "../lib/display-elements";
import {Avatar, Card, CardContent, CardHeader, CircularProgress, Collapse, Divider, IconButton, IconButtonProps, styled} from "@mui/material";
import {ExpandMore} from "@mui/icons-material";
import {ChatDisplayElement} from "./chat-display-element";
import {useState} from "react";
import BuildCircleIcon from '@mui/icons-material/BuildCircle';

interface ExpandMoreDivProps extends IconButtonProps {
  expand: boolean;
}

const ExpandMoreDiv = styled((props: ExpandMoreDivProps) => {
  return <IconButton {...props} />;
})(({theme, expand}) => ({
  transform: !expand ? 'rotate(0deg)' : 'rotate(180deg)',
  marginLeft: 'auto',
  transition: theme.transitions.create('transform', {
    duration: theme.transitions.duration.shortest,
  }),
}));

export interface ToolCallElementProps {
  machineUrl: string
  element: ToolCallElement
  agentName: string
}

export const ToolCall = ({machineUrl, element, agentName}: ToolCallElementProps) => {
  const [expanded, setExpanded] = useState(false);

  const handleExpandClick = () => {
    setExpanded(!expanded);
  };

  return (
    <Card variant={"outlined"} sx={{marginTop: "12px"}}>
      <CardHeader
        sx={{padding: "4px 8px 4px 8px"}}
        avatar={
          element.is_agent
            ? <Avatar sx={{height: "24px", width: "24px"}} src="/img/eidolon_with_gradient.png"/>
            : <Avatar sx={{height: "24px", width: "24px"}}><BuildCircleIcon/></Avatar>
        }
        onClick={handleExpandClick}
        action={
          <div style={{display: "flex", alignItems: "center"}}>
            {element.is_active && <CircularProgress variant={"indeterminate"} size={"16px"}/>}
            <ExpandMoreDiv
              expand={expanded}
              aria-expanded={expanded}
              aria-label="show more"
            >
              <ExpandMore/>
            </ExpandMoreDiv>
          </div>
        }
        title={element.is_agent ? (element.title + " Agent") : element.title}
        subheader={element.sub_title}
      >
      </CardHeader>
      <Collapse in={expanded} timeout="auto" unmountOnExit>
        <CardContent>
          <Divider/>
          {element.children.map((child, index) => {
              if (index < element.children.length - 1 || child.type != "success") {
                return <ChatDisplayElement userImage={undefined} userName={undefined} machineUrl={machineUrl} key={index} rawElement={child} topLevel={false} agentName={agentName}/>
              }
            }
          )}
        </CardContent>
      </Collapse>
    </Card>

  )
}