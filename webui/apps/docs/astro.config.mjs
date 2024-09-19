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
import astroExpressiveCode from "astro-expressive-code";

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
    astroExpressiveCode(),
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
            '    posthog.init(\'phc_9lcmDyxVkji98ggIqy2XvyVcItnrgdrMQhZBFp6Du5d\',{api_host:\'https://app.posthog.com\'});\n'
        },
      ],
      social: {
        github: 'https://github.com/eidolon-ai/eidolon',
        youtube: 'https://www.youtube.com/channel/UCARP0MIGLlq9BArL6HG6eUg',
        discord: 'https://discord.gg/6kVQrHpeqG',
        linkedin: 'https://www.linkedin.com/company/august-data',
        'x.com': 'https://twitter.com/AgentSDK',
      },
      sidebar: [
        {label: 'Quickstart', link: '/docs/quickstart'},
        {
          label: 'How To',
          items: [
            {label: 'Authenticate LLMs', link: '/docs/howto/authenticate_llm'},
            {label: 'Swap out LLMs', link: '/docs/howto/swap_llm'},
            {label: 'Configure Agent-Agent Communication', link: '/docs/howto/communication'},
            {label: 'Configure Built-in Components', link: '/docs/howto/configure_builtins'},
            {label: 'Use References', link: '/docs/howto/using_references'},
            {label: 'Build Custom Agent Templates', link: '/docs/howto/build_custom_agents'},
          ],
        },
        {
          label: 'Recipes',
          items: [
            {label: 'Chatbot', link: '/docs/recipes/chatbot'},
            {label: 'Github Repo Expert', link: '/docs/recipes/repo-expert'},
            {label: 'S3 RAG', link: '/docs/recipes/s3-rag'},
            {label: 'Web Researcher Chatbot', link: '/docs/recipes/web-researcher'},
            // {label: 'K8 Assistant', link: '/docs/recipes/under-construction'},
            // {label: 'Venture Search', link: '/docs/recipes/under-construction'},
            // {label: 'Github Repo Expert', link: '/docs/recipes/under-construction'},
            // {label: 'Local File Rag', link: '/docs/recipes/under-construction'},
          ],
        },
        {
          label: 'Builtin Components',
          items: [
            // ### Start Components ###
            {
              label: 'Resource', collapsed: true, items: [
                {label: 'Overview', link: '/docs/components/resource/overview'},
                {label: 'AgentResource', link: '/docs/components/resource/agentresource'},
                {label: 'MachineResource', link: '/docs/components/resource/machineresource'},
                {label: 'ReferenceResource', link: '/docs/components/resource/referenceresource'},
              ]
            },
            {
              label: 'SymbolicMemory', collapsed: true, items: [
                {label: 'Overview', link: '/docs/components/symbolicmemory/overview'},
                {label: 'LocalSymbolicMemory', link: '/docs/components/symbolicmemory/localsymbolicmemory'},
                {label: 'MongoSymbolicMemory', link: '/docs/components/symbolicmemory/mongosymbolicmemory'},
              ]
            },
            {
              label: 'SimilarityMemory', collapsed: true, items: [
                {label: 'Overview', link: '/docs/components/similaritymemory/overview'},
                {label: 'SimilarityMemoryImpl', link: '/docs/components/similaritymemory/similaritymemoryimpl'},
              ]
            },
            {
              label: 'FileMemoryBase', collapsed: true, items: [
                {label: 'Overview', link: '/docs/components/filememorybase/overview'},
                {label: 'AzureFileMemory', link: '/docs/components/filememorybase/azurefilememory'},
                {label: 'FileMemory', link: '/docs/components/filememorybase/filememory'},
                {label: 'LocalFileMemory', link: '/docs/components/filememorybase/localfilememory'},
                {label: 'S3FileMemory', link: '/docs/components/filememorybase/s3filememory'},
              ]
            },
            {
              label: 'Agents', collapsed: true, items: [
                {label: 'Overview', link: '/docs/components/agents/overview'},
                {label: 'APIAgent', link: '/docs/components/agents/apiagent'},
                {label: 'RetrieverAgent', link: '/docs/components/agents/retrieveragent'},
                {label: 'SimpleAgent', link: '/docs/components/agents/simpleagent'},
                {label: 'SqlAgent', link: '/docs/components/agents/sqlagent'},
              ]
            },
            {
              label: 'APU', collapsed: true, items: [
                {label: 'Overview', link: '/docs/components/apu/overview'},
                {label: 'ClaudeHaiku', link: '/docs/components/apu/claudehaiku'},
                {label: 'ClaudeOpus', link: '/docs/components/apu/claudeopus'},
                {label: 'ClaudeSonnet', link: '/docs/components/apu/claudesonnet'},
                {label: 'ConversationalAPU', link: '/docs/components/apu/conversationalapu'},
                {label: 'GPT3.5-turbo', link: '/docs/components/apu/gpt3_5-turbo'},
                {label: 'GPT4-turbo', link: '/docs/components/apu/gpt4-turbo'},
                {label: 'GPT4o', link: '/docs/components/apu/gpt4o'},
                {label: 'GPT4o-mini', link: '/docs/components/apu/gpt4o-mini'},
                {label: 'GPTo1Preview', link: '/docs/components/apu/gpto1preview'},
                {label: 'Llamma3-8b', link: '/docs/components/apu/llamma3-8b'},
                {label: 'MistralLarge', link: '/docs/components/apu/mistrallarge'},
                {label: 'MistralMedium', link: '/docs/components/apu/mistralmedium'},
                {label: 'MistralSmall', link: '/docs/components/apu/mistralsmall'},
              ]
            },
            {
              label: 'LLMUnit', collapsed: true, items: [
                {label: 'Overview', link: '/docs/components/llmunit/overview'},
                {label: 'AnthropicLLMUnit', link: '/docs/components/llmunit/anthropicllmunit'},
                {label: 'MistralGPT', link: '/docs/components/llmunit/mistralgpt'},
                {label: 'OllamaLLMUnit', link: '/docs/components/llmunit/ollamallmunit'},
                {label: 'OpenAIGPT', link: '/docs/components/llmunit/openaigpt'},
                {label: 'ToolCallLLMWrapper', link: '/docs/components/llmunit/toolcallllmwrapper'},
              ]
            },
            {
              label: 'LLMModel', collapsed: true, items: [
                {label: 'Overview', link: '/docs/components/llmmodel/overview'},
                {label: 'LLMModel', link: '/docs/components/llmmodel/llmmodel'},
                {label: 'claude-3-5-sonnet-20240620', link: '/docs/components/llmmodel/claude-3-5-sonnet-20240620'},
                {label: 'claude-3-haiku-20240307', link: '/docs/components/llmmodel/claude-3-haiku-20240307'},
                {label: 'claude-3-opus-20240229', link: '/docs/components/llmmodel/claude-3-opus-20240229'},
                {label: 'claude-3-sonnet-20240229', link: '/docs/components/llmmodel/claude-3-sonnet-20240229'},
                {label: 'gpt-3.5-turbo', link: '/docs/components/llmmodel/gpt-3_5-turbo'},
                {label: 'gpt-4-turbo', link: '/docs/components/llmmodel/gpt-4-turbo'},
                {label: 'gpt-4o', link: '/docs/components/llmmodel/gpt-4o'},
                {label: 'gpt-4o-mini', link: '/docs/components/llmmodel/gpt-4o-mini'},
                {label: 'gpt-o1-preview', link: '/docs/components/llmmodel/gpt-o1-preview'},
                {label: 'llama3-8b', link: '/docs/components/llmmodel/llama3-8b'},
                {label: 'mistral-large-latest', link: '/docs/components/llmmodel/mistral-large-latest'},
                {label: 'mistral-medium-latest', link: '/docs/components/llmmodel/mistral-medium-latest'},
                {label: 'mistral-small-latest', link: '/docs/components/llmmodel/mistral-small-latest'},
              ]
            },
            {
              label: 'LogicUnit', collapsed: true, items: [
                {label: 'Overview', link: '/docs/components/logicunit/overview'},
                {label: 'ApiLogicUnit', link: '/docs/components/logicunit/apilogicunit'},
                {label: 'AudioUnit', link: '/docs/components/logicunit/audiounit'},
                {label: 'Browser', link: '/docs/components/logicunit/browser'},
                {label: 'OpenAIImageUnit', link: '/docs/components/logicunit/openaiimageunit'},
                {label: 'OpenAiSpeech', link: '/docs/components/logicunit/openaispeech'},
                {label: 'Search', link: '/docs/components/logicunit/search'},
                {label: 'VectaraSearch', link: '/docs/components/logicunit/vectarasearch'},
                {label: 'WebSearch', link: '/docs/components/logicunit/websearch'},
              ]
            },
            {
              label: 'DocumentManager', collapsed: true, items: [
                {label: 'Overview', link: '/docs/components/documentmanager/overview'},
                {label: 'DocumentManager', link: '/docs/components/documentmanager/documentmanager'},
              ]
            },
            {
              label: 'DocumentLoader', collapsed: true, items: [
                {label: 'Overview', link: '/docs/components/documentloader/overview'},
                {label: 'AzureLoader', link: '/docs/components/documentloader/azureloader'},
                {label: 'FilesystemLoader', link: '/docs/components/documentloader/filesystemloader'},
                {label: 'GitHubLoader', link: '/docs/components/documentloader/githubloader'},
                {label: 'S3Loader', link: '/docs/components/documentloader/s3loader'},
              ]
            },
            // ### End Components ###
          ]
        },
        {
          label: 'FAQ', link: '/docs/faq'
        },
        {
          label: 'Architecture',
          collapsed: true,
          items: [
            {label: 'Introduction', link: '/docs/architecture/introduction'},
            {label: 'Fundamentals', link: '/docs/architecture/fundamentals'},
            {label: 'Agent Program', link: '/docs/architecture/agent_program'},
            {label: 'Agent Processing Unit', link: '/docs/architecture/agent_apu'},
            {label: 'AgentOS', link: '/docs/architecture/agent_os'},
            {label: 'Conclusion', link: '/docs/architecture/conclusion'},
          ],
        },
        {label: 'Contributing', link: '/docs/contributing'},
      ],
      editLink: {
        baseUrl: 'https://github.com/eidolon-ai/eidolon/tree/main/webui/apps/docs',
      },
    }),
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
  },
  redirects: {
    // '/old-page': '/new-page'
    '/docs/components/simple_agent/': '/docs/components/agents/simpleagent/',
    '/docs/components/simple_agent#defining-actions': '/docs/components/agents/simpleagent#51-actiondefinition',
    '/docs/howto/customize_builtins/': '/docs/howto/configure_builtins/',
    '/docs/howto/custom_agents/': '/docs/howto/build_custom_agents/'
  }
});
