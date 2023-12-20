import {defineConfig} from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
    site: 'https://eidolon-ai.github.io/eidOS/',
    base: '/eidOS',
    integrations: [
        starlight({
            title: 'Eidolon',
            social: {
                github: 'https://github.com/eidolon-ai/eidOS',
            },
            sidebar: [
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
				{
					label: 'Getting Started',
					items: [
						{ label: 'Quickstart', link: '/getting_started/quickstart/' },
						{ label: 'Advanced', link: '/getting_started/advanced/' },
					],
// 					autogenerate: { directory: 'getting_started'},
                },
            ],
        }),
    ],
});
