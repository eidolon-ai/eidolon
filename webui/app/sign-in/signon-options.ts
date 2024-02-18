'use server'

const providerTypes = process.env.EIDOLON_AUTH_PROVIDERS?.split(',') || []

export async function getSigninOptions() {
  console.log("tt", providerTypes)
  return providerTypes
}
