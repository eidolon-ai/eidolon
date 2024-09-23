import { defineEcConfig } from 'astro-expressive-code'
import { pluginCollapsibleSections } from '@expressive-code/plugin-collapsible-sections'

export default defineEcConfig({
  // Example: Using a custom plugin (which makes this `ec.config.mjs` file necessary)
  plugins: [pluginCollapsibleSections()],
  frames: {
  },
  // ... any other options you want to configure
})
