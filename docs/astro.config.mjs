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
                                {label:'Setup', link:'/getting_started/quickstart/setup'},
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
                        },
                        {label: 'Tutorials', link: '/getting_started/tutorials/'},
                        {label: 'References', link: '/getting_started/references/'},
                    ],
// 					autogenerate: { directory: 'getting_started'},
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
