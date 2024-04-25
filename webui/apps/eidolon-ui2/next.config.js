/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
 modularizeImports: {
  'react-icons/ai': {
    transform: 'react-icons/ai/{{member}}',
  },
},
  // reactStrictMode: false,
  output: 'standalone',
};

module.exports = nextConfig;
