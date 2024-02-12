import {defineConfig} from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
    site: 'https://www.eidolonai.com',
    integrations: [
        starlight({
            title: 'Eidolon',
            // components: {
            //   Hero: './src/components/NewHero.astro',
            // },
            favicon: '/favicon.ico',
            social: {
                github: 'https://github.com/eidolon-ai/eidolon',
                youtube: 'https://www.youtube.com/channel/UCARP0MIGLlq9BArL6HG6eUg',
                discord: 'https://discord.gg/Wk3ntSna',
            },
            sidebar: [
				{
					label: 'Getting Started',
					items: [
						{ label: 'Quickstart', link: '/getting_started/quickstart/' },
						{ label: 'Next Steps', link: '/getting_started/slowstart/' },
					],
// 					autogenerate: { directory: 'getting_started'},
                },
                {
                    label: 'Architecture',
                    items: [
                        { label: 'Introduction', link: '/architecture/introduction/' },
                        { label: 'Fundamentals', link: '/architecture/fundamentals/' },
                        {label: 'Agent Program', link: '/architecture/agent_program/' },
						{ label: 'Agent CPU', link: '/architecture/agent_cpu/' },
						{ label: 'AgentOS', link: '/architecture/agent_os/' },
						{ label: 'Conclusion', link: '/architecture/conclusion/' },
					],
				},
            ],
        }),
    ],
});
