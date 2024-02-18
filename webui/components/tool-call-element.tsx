import {ToolCallElement} from "@/lib/display-elements";
import {OperationInfo} from "@/lib/types";
import {Avatar, Card, CardActions, CardContent, CardHeader, CircularProgress, Collapse, Divider, IconButton, IconButtonProps, styled} from "@mui/material";
import * as React from "react";
import CodeOffRoundedIcon from "@mui/icons-material/CodeOffRounded";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import {ChatDisplayElement} from "@/components/chat-events";

interface ExpandMoreProps extends IconButtonProps {
  expand: boolean;
}

const ExpandMore = styled((props: ExpandMoreProps) => {
  const {expand, ...other} = props;
  return <IconButton {...other} />;
})(({theme, expand}) => ({
  transform: !expand ? 'rotate(0deg)' : 'rotate(180deg)',
  marginLeft: 'auto',
  transition: theme.transitions.create('transform', {
    duration: theme.transitions.duration.shortest,
  }),
}));

export interface ToolCallElementProps {
  element: ToolCallElement
  agentName: string
  handleAction: (operation: OperationInfo, data: Record<string, any>) => void
}

export const ToolCall = ({element, agentName, handleAction}: ToolCallElementProps) => {
  const [expanded, setExpanded] = React.useState(false);

  const handleExpandClick = () => {
    setExpanded(!expanded);
  };

  return (
    <Card variant={"outlined"} sx={{marginTop: "12px"}}>
      <CardHeader
        sx={{padding: "12px 8px 0px 8px"}}
        avatar={
          element.is_agent
            ? <Avatar sx={{height: "32px", width: "32px"}} src="/eidolon_with_gradient.png"/>
            : <Avatar sx={{height: "32px", width: "32px"}}><CodeOffRoundedIcon/></Avatar>
        }
        onClick={handleExpandClick}
        action={
          <div style={{display: "flex", alignItems: "center"}}>
            {element.is_active && <CircularProgress variant={"indeterminate"} size={"16px"}/>}
            <ExpandMore
              expand={expanded}
              aria-expanded={expanded}
              aria-label="show more"
            >
              <ExpandMoreIcon/>
            </ExpandMore>
          </div>
        }
        title={element.is_agent ? (element.title + " Agent") : element.title}
        subheader={element.sub_title}
      >
      </CardHeader>
      <CardActions disableSpacing>
      </CardActions>
      <Collapse in={expanded} timeout="auto" unmountOnExit>
        <CardContent>
          <Divider/>
          {element.children.map((child, index) => {
              if (index < element.children.length - 1 || child.type != "success") {
                return <ChatDisplayElement key={index} rawElement={child} topLevel={false} agentName={agentName}
                                           handleAction={handleAction}/>
              }
            }
          )}
        </CardContent>
      </Collapse>
    </Card>

  )
}