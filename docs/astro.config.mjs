import {defineConfig} from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
    site: 'https://www.eidolonai.com',
    integrations: [
        starlight({
            title: 'Eidolon',
            components: {
                SiteTitle: './src/components/FixedTitle.astro',
            },
//             components: {
//                 todo ThemeSelect has issues finding StarlightThemeProvider
//                 ThemeSelect: './src/components/ThemeSelect.astro',
//                 Hero: './src/components/NewHero.astro',
//             },
            // editLink: {
            //      todo Edit Page leads to 404
            //     baseUrl: 'https://github.com/eidolon-ai/eidolon/tree/main/docs/src/content/docs',
            // },
            favicon: '/favicon.ico',
            head: [
                {
                    tag: 'script',
                    attrs: {
                        // Tweaks to the script URL or attributes can be made here.
                        src: 'https://www.googletagmanager.com/gtag/js?id=G-ES73QFGWZ1',
                        async: true,
                    },
                },
                {
                    tag: 'script',
                    content: '  window.dataLayer = window.dataLayer || [];\n' +
                        '  function gtag(){dataLayer.push(arguments);}\n' +
                        '  gtag(\'js\', new Date());\n' +
                        '\n' +
                        '  gtag(\'config\', \'G-ES73QFGWZ1\');\n'
                },
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
                'x.com': 'https://x.com/AgentSaaS',
            },
            sidebar: [
                {
                    label: 'Introduction', link: '/introduction'
                },
                {
                    label: 'Getting Started',
                    items: [
                        {
                            label: 'Quickstart', 
                            items: [
                                {label:'Introduction', link:'/getting_started/quickstart/introduction'},
                                {label:'Prerequisites', link:'/getting_started/quickstart/prereq'},
                                {label:'Create an Agent', link:'/getting_started/quickstart/create'},
                                {label:'Run and Try', link:'/getting_started/quickstart/run'},
                            ]
                        },
                        {   
                            label: 'Demos',
                            items: [
                                {label:'Introduction', link: '/getting_started/demos/introduction'},
                                {label:'Chatbot Demo', link: '/getting_started/demos/swifties'}
                            ] 
                        },
                        {   
                            label: 'Tutorials',
                            items: [
                                {label:'Introduction', link: '/getting_started/tutorials/introduction'},
                                {label:'EidolonGPT', link: '/getting_started/tutorials/gpt'},
                                {label:'Code Search', link: '/getting_started/tutorials/docs'}
                            ] 
                        }
                    ],
// 					autogenerate: { directory: 'getting_started'},
                },
                {
                    label: 'References',
                    items: [
                        {label: 'Introduction', link: '/references/introduction/'},
                        {label: 'Setup', link: '/references/setup'},
                        {label: 'Agent Communication', link: '/references/communication'},
                        {label: 'Custom Agents', link: '/references/custom'},
                        {label: 'Pluggable Resources', link: '/references/pluggable'},
                        {label: 'Defining a Machine', link: '/references/defining'},
                    ],
                },
                {
                    label: 'Architecture',
                    items: [
                        {label: 'Introduction', link: '/architecture/introduction/'},
                        {label: 'Fundamentals', link: '/architecture/fundamentals/'},
                        {label: 'Agent Program', link: '/architecture/agent_program/'},
                        {label: 'Agent CPU', link: '/architecture/agent_cpu/'},
                        {label: 'AgentOS', link: '/architecture/agent_os/'},
                        {label: 'Conclusion', link: '/architecture/conclusion/'},
                    ],
                },
            ],
        }),
    ],
});
