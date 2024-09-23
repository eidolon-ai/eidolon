/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: true,
    devIndicators:{
        autoPrerender: false,
    },
    output: 'standalone',
};

export default nextConfig;