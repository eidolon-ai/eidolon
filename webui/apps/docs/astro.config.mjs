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

/// <reference path="../node_modules/@astrojs/starlight/virtual.d.ts"/>

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
      components: {
        "PageFrame": "~/components/StarlightPageFame.astro",
        "Header": "~/components/DocsHeader.astro",
      },
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
          label: 'Quickstart',
          autogenerate: { directory: '/docs/quickstart' },
        },
        {
          label: 'Recipes',
          items: [
            {label: 'Chatbot', link: 'todo'},
            {label: 'Github Repo Expert', link: 'todo'},
            {label: 'K8 Assistant', link: 'todo'},
            {label: 'Venture Search', link: 'todo'},
            {label: 'Github Repo Expert', link: 'todo'},
            {label: 'Local File Rag', link: 'todo'},
          ],
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
