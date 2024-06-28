/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: true,
    modularizeImports: {
        'react-icons/ai': {
            transform: 'react-icons/ai/{{member}}',
        },
    },
    output: 'standalone',
};

export default nextConfig;