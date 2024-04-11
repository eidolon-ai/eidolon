import path from 'path';
import {fileURLToPath} from 'url';
import {defineConfig, squooshImageService} from 'astro/config';
import sitemap from '@astrojs/sitemap';
import tailwind from '@astrojs/tailwind';
import mdx from '@astrojs/mdx';
import partytown from '@astrojs/partytown';
import icon from 'astro-icon';
import compress from 'astro-compress';
import astrowind from './src/integration';
import {readingTimeRemarkPlugin, responsiveTablesRehypePlugin, lazyImagesRehypePlugin} from './src/utils/frontmatter.mjs';
import starlight from "@astrojs/starlight";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const hasExternalScripts = false;
const whenExternalScripts = (items = []) => hasExternalScripts ? Array.isArray(items) ? items.map(item => item()) : [items()] : [];

// https://astro.build/config
export default defineConfig({
  output: 'static',
  integrations: [tailwind({
    applyBaseStyles: false
  }), sitemap(), icon({
    include: {
      tabler: ['*'],
      'flat-color-icons': ['template', 'gallery', 'approval', 'document', 'advertising', 'currency-exchange', 'voice-presentation', 'business-contact', 'database']
    }
  }), ...whenExternalScripts(() => partytown({
    config: {
      forward: ['dataLayer.push']
    }
  })), compress({
    CSS: true,
    HTML: {
      'html-minifier-terser': {
        removeAttributeQuotes: false
      }
    },
    Image: false,
    JavaScript: true,
    SVG: false,
    Logger: 1
  }),
    astrowind(),
    starlight({
      title: "Introduction",
      disable404Route: true,
      components: {},
      social: {
        github: 'https://github.com/eidolon-ai/eidolon',
        youtube: 'https://www.youtube.com/channel/UCARP0MIGLlq9BArL6HG6eUg',
        discord: 'https://discord.gg/6kVQrHpeqG',
        linkedin: 'https://www.linkedin.com/company/august-data/',
        'x.com': 'https://twitter.com/AgentSDK',
      },
      sidebar: [
        {
          label: 'Introduction', link: '/docs/introduction'
        },
        {
          label: 'Getting Started',
          items: [
            {
              label: 'Quickstart',
              items: [
                {label: 'Introduction', link: '/docs/getting_started/quickstart/introduction'},
                {label: 'Prerequisites', link: '/docs/getting_started/quickstart/prereq'},
                {label: 'Create an Agent', link: '/docs/getting_started/quickstart/create'},
                {label: 'Run and Try', link: '/docs/getting_started/quickstart/run'},
              ]
            },
            {
              label: 'Demos',
              items: [
                {label: 'Introduction', link: '/docs/getting_started/demos/introduction'},
                {label: 'Chatbot Demo', link: '/docs/getting_started/demos/swifties'}
              ]
            },
            {
              label: 'Tutorials',
              items: [
                {label: 'Introduction', link: '/docs/getting_started/tutorials/introduction'},
                {label: 'EidolonGPT', link: '/docs/getting_started/tutorials/gpt'},
                {label: 'Code Search', link: '/docs/getting_started/tutorials/docs'}
              ]
            }
          ],
// 					autogenerate: { directory: 'getting_started'},
        },
        {
          label: 'References',
          items: [
            {label: 'Introduction', link: '/docs/references/introduction/'},
            {label: 'Setup', link: '/docs/references/setup'},
            {label: 'Agent Communication', link: '/docs/references/communication'},
            {label: 'Custom Agents', link: '/docs/references/custom'},
            {label: 'Pluggable Resources', link: '/docs/references/pluggable'},
            {label: 'Defining a Machine', link: '/docs/references/defining'},
          ],
        },
        {
          label: 'Architecture',
          items: [
            {label: 'Introduction', link: '/docs/architecture/introduction/'},
            {label: 'Fundamentals', link: '/docs/architecture/fundamentals/'},
            {label: 'Agent Program', link: '/docs/architecture/agent_program/'},
            {label: 'Agent CPU', link: '/docs/architecture/agent_cpu/'},
            {label: 'AgentOS', link: '/docs/architecture/agent_os/'},
            {label: 'Conclusion', link: '/docs/architecture/conclusion/'},
          ],
        },
      ]
    })
  ],
  image: {
    service: squooshImageService()
  },
  markdown: {
    remarkPlugins: [readingTimeRemarkPlugin],
    rehypePlugins: [responsiveTablesRehypePlugin, lazyImagesRehypePlugin]
  },
  vite: {
    resolve: {
      alias: {
        '~': path.resolve(__dirname, './src')
      }
    }
  }
});
