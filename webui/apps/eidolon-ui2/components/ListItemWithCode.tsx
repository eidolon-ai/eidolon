'use client'

import {ListItem, ListItemText, Typography} from "@mui/material";
import {useState} from "react";
import {EidolonMarkdown} from "@eidolon-ai/components/client";

interface ListItemWithCodeProps {
  title: string
  caption?: string
  text: string
  configFile?: string
  configFileExternalLink?: string
  builtinAgentType?: string
  codeFile?: string
  codeFileExternalLink?: string
}

export default function ListItemWithCode(props: ListItemWithCodeProps) {
  const [configFileContents, setConfigFileContents] = useState<string | undefined>(undefined)
  const [codeFileContents, setCodeFileContents] = useState<string | undefined>(undefined)
  const [showingConfiguration, setShowingConfiguration] = useState(false)
  const [showingCode, setShowingCode] = useState(false)

  async function showConfiguration() {
    if (props.configFile) {
      if (!configFileContents) {
        const response = await fetch(props.configFile)
        if (response.ok) {
          setConfigFileContents(await response.text())
        }
      }
      setShowingCode(false)
      setShowingConfiguration(!showingConfiguration)
    }
  }

  async function showCode() {
    if (props.codeFile) {
      if (!codeFileContents) {
        const response = await fetch(props.codeFile)
        if (response.ok) {
          setCodeFileContents(await response.text())
        }
      }
      setShowingConfiguration(false)
      setShowingCode(!showingCode)
    }
  }

  function getPathRoot(path: string) {
    return path.slice(path.lastIndexOf('/') + 1)
  }

  return (
    <ListItem>
      <div style={{position: "relative", width: "100%"}}>
        {(showingConfiguration || showingCode) && (
          <div style={{float: "right", display: "block", maxWidth: "50%", overflow: "auto", maxHeight: "400px", border: "1px dashed #aaa"}}>
            <EidolonMarkdown showLineNumbers={true} machineUrl={""}>
              {'```yaml\n' + (showingConfiguration ? configFileContents : codeFileContents) + "\n```"}
            </EidolonMarkdown>
          </div>
        )}
        <div style={{maxWidth: showingConfiguration ? "50%" : "100%"}}>
          <ListItemText>
            <div style={{display: "flex", alignItems: "start"}}>
              <Typography variant={"h6"}><b>{props.title}</b></Typography>
              {props.caption && (<Typography variant={"caption"}> {props.caption}</Typography>)}
            </div>
            {props.configFile && (
              <Typography sx={{marginLeft: "16px", display: "flex", alignItems: "center"}} variant={"body2"}>
                <Typography sx={{marginRight: "8px"}} fontWeight={"bold"}>configuration:</Typography>
                {getPathRoot(props.configFile)}
                &nbsp;<a style={{backgroundColor: showingConfiguration ? "#88aaaa" : "inherit"}} onClick={showConfiguration}>👁</a>️&nbsp;<a href={props.configFileExternalLink} target="_blank">🔗</a>
              </Typography>
            )}
            {props.codeFile && (
              <Typography sx={{marginLeft: "16px", display: "flex", alignItems: "center"}} variant={"body2"}>
                <Typography sx={{marginRight: "8px"}} fontWeight={"bold"}>code:</Typography>
                {getPathRoot(props.codeFile)}
                &nbsp;<a style={{backgroundColor: showingCode ? "#88aaaa" : "inherit"}} onClick={showCode}>👁</a>️&nbsp;<a href={props.codeFileExternalLink} target="_blank">🔗</a>
              </Typography>
            )}
            {props.builtinAgentType && (
              <Typography sx={{marginLeft: "16px", display: "flex", alignItems: "center"}} variant={"body2"}>
                <Typography sx={{marginRight: "8px"}} fontWeight={"bold"}>builtin agent:</Typography>
                {props.builtinAgentType}
                &nbsp;<a href={props.codeFileExternalLink} target="_blank">🔗</a>
              </Typography>
            )}
            <Typography sx={{marginTop: "16px"}} variant={"body1"}>
              {props.text}
            </Typography>
          </ListItemText>
        </div>
      </div>
    </ListItem>
  )
}