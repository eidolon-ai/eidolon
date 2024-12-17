import {getAsset, getBlogPermalink, getPermalink} from './utils/permalinks';

export const headerData = {
    links: [
      {
        text: 'Home',
        href: '/',
      },
      {
        text: 'Examples',
        href: '/docs/recipes/chatbot',
      },
      {
        text: 'Documentation',
        href: '/docs/quickstart',
      },
      {
        text: 'Blog',
        href: getBlogPermalink(),
      },
      {
        text: 'FAQ',
        href: '/docs/faq',
      },
      {
        text: 'Videos',
        href: 'https://www.youtube.com/channel/UCARP0MIGLlq9BArL6HG6eUg',
        newTab: true,
      }
    ],
    actions: [
    ],
    showRssFeed:
      false
  }

export const footerData = {
    links: [
    {
      title: 'Company',
      links: [
        {
          text: 'Team',
          href: getPermalink('/about'),
        },
        {
          text: 'Terms of Service',
          href: getPermalink('/terms'),
        },
      ],
    },
    {
      title: 'Resources',
      links: [
        {
          text: 'Docs',
          href: getPermalink('/docs/quickstart'),
        },
        {
          text: 'Blog',
          href: getBlogPermalink(),
        },
        {
          text: 'FAQs',
          href: getPermalink('/docs/faq'),
        },
        {
          text: 'GitHub',
          href: 'https://github.com/eidolon-ai/eidolon',
        },
      ],
    },
    {
      title: 'Community',
      links: [
        {
          text: 'Discord',
          href: 'https://discord.gg/6kVQrHpeqG',
        },
        // {
        //   text: 'Twitter / X',
          // href: 'https://twitter.com/AgentServer',
        // },
        {
          text: 'Youtube',
          href: 'https://www.youtube.com/channel/UCARP0MIGLlq9BArL6HG6eUg',
        },
        {
          text: 'LinkedIn',
          href: 'https://www.linkedin.com/company/august-data/',
        },
      ],
    },
   ],
  socialLinks: [
    // {ariaLabel: 'X', icon: 'tabler:brand-x', href: 'https://twitter.com/AgentSDK'},
    {ariaLabel: 'LinkedIn', icon: 'tabler:brand-linkedin', href: 'https://www.linkedin.com/company/august-data/'},
    {ariaLabel: 'Discord', icon: 'tabler:brand-discord', href: 'https://discord.gg/6kVQrHpeqG'},
    {ariaLabel: 'YouTube', icon: 'tabler:brand-youtube', href: 'https://www.youtube.com/channel/UCARP0MIGLlq9BArL6HG6eUg'},
    {ariaLabel: 'RSS', icon: 'tabler:rss', href: getAsset('/rss.xml')},
    {ariaLabel: 'Github', icon: 'tabler:brand-github', href: 'https://github.com/eidolon-ai/eidolon'},
  ],
  // footNote: `
  //   <span class="w-5 h-5 md:w-6 md:h-6 md:-mt-0.5 bg-cover mr-1.5 rtl:mr-0 rtl:ml-1.5 float-left rtl:float-right rounded-sm bg-[url(https://onwidget.com/favicon/favicon-32x32.png)]"></span>
  //   Made by <a class="text-blue-600 underline dark:text-muted" href="https://onwidget.com/"> onWidget</a> · All rights reserved.
  // `,
};
