import { defineConfig } from '@hey-api/openapi-ts'

export default defineConfig({
  client: 'fetch',
  input: 'http://localhost:8527/openapi.json',
  output: 'src',
})
