import {Box, Button, TextField} from "@mui/material";
import * as React from "react";

export interface StartProcessInputFormProps {
  handleStartProcess: (ventureSite: string) => void
  loading: boolean
}

export default function ({handleStartProcess, loading}: StartProcessInputFormProps) {
  const [ventureSite, setVentureSite] = React.useState<string>('https://10tfund.com/portfolio/')
  const [ventureSiteError, setVentureSiteError] = React.useState(false)

  return (
    <Box
      component="form"
      sx={{
        width: "100%",
        display: "flex",
        flexDirection: "column",
        '& .MuiTextField-root': {m: 2, width: '100%', maxWidth: '800px'},
        '& .MuiButton-root': {alignSelf: 'flex-end', m: 2},
      }}
      autoComplete="off"
    >
      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
        }}
      >
        <TextField
          label="Venture Site"
          required={true}
          value={ventureSite}
          disabled={loading}
          onChange={(e) => {
            setVentureSite(e.target.value)
            setVentureSiteError(!e.target.validity.valid)
          }}
          onBlur={(e) => {
            setVentureSiteError(!e.target.validity.valid)
          }}
          helperText={"Enter the URL for the site that contains the portfolio companies you want to search for."}
          size="medium"
          error={ventureSiteError}
          variant="standard"
          inputMode={"url"}
          inputProps={{
            // a valid URL pattern, see https://url.spec.whatwg.org/#valid-url
            pattern: "https://.*",
          }}
        />
      </Box>
      <Button
        variant="contained"
        disabled={ventureSiteError || loading}
        onClick={() => {
          handleStartProcess(ventureSite)
        }}
      >Go</Button>
    </Box>
  )
}
