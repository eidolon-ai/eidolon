'use client'

import {Box, Button, TextField} from "@mui/material";

export interface SigninFormData {
  doSignin: (providerId: string, formData: FormData) => Promise<void>
  provider: any
}

export default function SigninForm({provider, doSignin}: SigninFormData) {
  const csrfToken = "csrfToken"
  const providerLogoPath = "https://authjs.dev/img/providers"

  async function handleSubmit(providerId: string, event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const form = event.currentTarget
    const formData = new FormData(form)
    await doSignin(providerId, formData)
  }

  let bg, brandColor, logo
  if (provider.type === "oauth" || provider.type === "oidc") {
    bg = provider.style?.bg || "#fff"
    brandColor = provider.style?.brandColor
    logo = provider.style?.logo ?? `${providerLogoPath}/${provider.id}.svg`
  }
  let credentials = provider.credentials
  if (provider.type === "email") {
    credentials = {
      email: {
        label: "Email",
        type: "email",
        placeholder: "email@example.com"
      }
    }
  }

  const color = brandColor ?? bg ?? "#fff"
  return (
    <form onSubmit={(e) => handleSubmit(provider.id, e)} method="POST" style={{width: "100%"}}>
      <Box key={provider.id} sx={{display: "flex", alignContent: "center", justifyContent: "center", margin: "8px", width: "100%"}}>
        {provider.type === "oauth" || provider.type === "oidc" ? (
          <Button
            type="submit"
            color={"primary"}
            sx={{borderColor: "#555", color: color + " !important"}}
            variant={"outlined"}
            autoCapitalize={"false"}
            startIcon={(
              <img
                alt="provider-logo"
                loading="lazy"
                height={24}
                width={24}
                id="provider-logo"
                src={logo}
              />
            )}
          >
            <span style={{textTransform: "none"}}>Sign in with {provider.name}</span>
          </Button>
        ) : null}

        {(provider.type === "credentials" || provider.type == "email") && (
          <Box sx={{display: "flex", flexDirection: "column", width: "100%", alignItems: "end"}}>
            <Box sx={{display: "flex", flexDirection: "column", width: "100%"}}>
              <input type="hidden" name="csrfToken" value={csrfToken}/>
              {Object.keys(credentials).map((credential) => {
                return (
                  <TextField id={`input-${credential}-for-${provider.id}-provider`}
                             variant="standard"
                             required={true}
                             label={credentials[credential].label ?? credential}
                             placeholder={credentials[credential].placeholder ?? ""}
                             name={credential}
                             type={credentials[credential].type ?? "text"}
                  />
                )
              })}
            </Box>
            <Button
              id="submitButton"
              color={"primary"}
              sx={{borderColor: "#555", width: "fit-content", marginTop: "16px"}}
              variant={"outlined"}
              type="submit"
            >
              <span style={{textTransform: "none"}}>Sign in</span>
            </Button>
          </Box>
        )}
        {provider.type === "webauthn" && (
          <Box>
            <input type="hidden" name="csrfToken" value={csrfToken}/>
            {Object.keys(provider.formFields).map((field) => {
              return (
                <div key={`input-group-${provider.id}`}>
                  <label
                    className="section-header"
                    htmlFor={`input-${field}-for-${provider.id}-provider`}
                  >
                    {provider.formFields[field].label ?? field}
                  </label>
                  <input
                    name={field}
                    data-form-field
                    id={`input-${field}-for-${provider.id}-provider`}
                    type={provider.formFields[field].type ?? "text"}
                    placeholder={
                      provider.formFields[field].placeholder ?? ""
                    }
                    {...provider.formFields[field]}
                  />
                </div>
              )
            })}
            <button
              id={`submitButton-${provider.id}`}
              type="submit"
              tabIndex={0}
            >
              Sign in with {provider.name}
            </button>
          </Box>
        )}
      </Box>
    </form>

  )
}