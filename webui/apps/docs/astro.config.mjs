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
  trailingSlash: 'never',
  'build.format': 'file',
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
      head: [
        {
          tag: 'script',
          content: '    !function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement("script")).type="text/javascript",p.async=!0,p.src=s.api_host+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],u.toString=function(t){var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e},u.people.toString=function(){return u.toString(1)+".people (stub)"},o="capture identify alias people.set people.set_once set_config register register_once unregister opt_out_capturing has_opted_out_capturing opt_in_capturing reset isFeatureEnabled onFeatureFlags getFeatureFlag getFeatureFlagPayload reloadFeatureFlags group updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures getActiveMatchingSurveys getSurveys onSessionId".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);\n' +
            '    posthog.init(\'phc_9lcmDyxVkji98ggIqy2XvyVcItnrgdrMQhZBFp6Du5d\',{api_host:\'https://app.posthog.com\'})\n'
        },
      ],
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
        {label: 'Prerequisites', link: '/docs/prereq/'},
        {label: 'Quickstart', link: '/docs/create/'},
        {
          label: 'How To',
          items: [
            {label: 'Launch the WebUI', link: '/docs/references/webui'},
            {label: 'Agent-Agent Communication', link: '/docs/references/communication'},
            {label: 'Component Customization', link: '/docs/references/pluggable'},
            {label: 'Custom Agent Templates', link: '/docs/references/custom_agents'},
            // {label: 'Custom Logic Units', link: '/docs/references/custom_logic_units'},
            {label: 'Custom Components', link: '/docs/references/using_references'},
          ],
        },
        {
          label: 'Recipes',
          items: [
            {label: 'Chatbot', link: '/docs/recipes/chatbot/'},
            {label: 'Github Repo Expert', link: '/docs/recipes/repo-expert/'},
            // {label: 'K8 Assistant', link: '/docs/recipes/under-construction/'},
            // {label: 'Venture Search', link: '/docs/recipes/under-construction/'},
            // {label: 'Github Repo Expert', link: '/docs/recipes/under-construction/'},
            // {label: 'Local File Rag', link: '/docs/recipes/under-construction/'},
          ],
        },
        {
          label: 'Builtin Components',
          items: [
            {
              label: 'Agent Templates', collapsed: true, items: [
                {label: 'SimpleAgent', link: '/docs/components/simple_agent'},
                {label: 'RetrieverAgent', link: '/docs/components/retriever_agent'},
              ]
            },
            {
              label: 'APU', collapsed: true, items: [
                {label: 'Overview', link: '/docs/components/apu/'},
                {label: 'ConversationalAPU', link: '/docs/components/conversational_apu/'},
              ]
            },
            {
              label: 'LLMUnit', collapsed: true, items: [
                {label: 'Overview', link: '/docs/components/llm_unit'},
                {label: 'OpenAIGPT', link: '/docs/components/llm_unit_openai'},
                {label: 'MistralGPT', link: '/docs/components/llm_unit_minstral'},
                {label: 'AnthropicLLMUnit', link: '/docs/components/llm_unit_anthropic'},
              ]
            },
            // {
            //   label: 'Logic Unit', collapsed: true, items: [
            //     {label: 'Logic Unit Overview', link: '/docs/recipes/under-construction/'},
            //     {label: 'Overview', link: '/docs/recipes/under-construction/'},
            //     {label: 'Search', link: '/docs/recipes/under-construction/'},
            //     {label: 'Browser', link: '/docs/recipes/under-construction/'},
            //   ]
            // },
          ]
        },
        {
          label: 'Architecture',
          items: [
            {label: 'Introduction', link: '/docs/architecture/introduction/'},
            {label: 'Fundamentals', link: '/docs/architecture/fundamentals/'},
            {label: 'Agent Program', link: '/docs/architecture/agent_program/'},
            {label: 'Agent Processing Unit', link: '/docs/architecture/agent_apu/'},
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
