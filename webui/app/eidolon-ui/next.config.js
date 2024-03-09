/** @type {import('next').NextConfig} */
module.exports = {
    reactStrictMode: true,
    images: {
        remotePatterns: [
            {
                protocol: "https",
                hostname: "**.googleusercontent.com",
                port: "",
                pathname: "/**",
            },
            {
                protocol: 'https',
                hostname: 'avatars.githubusercontent.com',
            }
        ],
    }
};

