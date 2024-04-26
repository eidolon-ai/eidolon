import {getAsset, getBlogPermalink} from './utils/permalinks';

export const headerData = {
    links: [
      {
        text: 'Docs',
        href: '/docs/introduction',
      },
      {
        text: 'Blog',
        href: getBlogPermalink(),
      },
      {
        text: 'Events',
        href: '#events',
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
      title: 'Product',
      links: [
        {text: 'Features', href: '#features'},
        {text: 'Documentation', href: '/docs/introduction'},
      ],
    },
    {
      title: 'Project',
      links: [
        {text: 'About', href: '/about'},
      ],
    },
  ],
  /*
    secondaryLinks: [
      { text: 'Terms', href: getPermalink('/terms') },
      { text: 'Privacy Policy', href: getPermalink('/privacy') },
    ],
  */
  socialLinks: [
    {ariaLabel: 'X', icon: 'tabler:brand-x', href: 'https://twitter.com/AgentSDK'},
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
