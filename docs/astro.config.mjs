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
                    label: 'Guides',
                    items: [
                        // Each item here is one entry in the navigation menu.
                        {label: 'Example Guide', link: '/guides/example/'},
                    ],
                },
                {
                    label: 'Reference',
                    autogenerate: {directory: 'reference'},
                },
            ],
        }),
    ],
});
