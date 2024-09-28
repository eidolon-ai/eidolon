/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./app/**/*.{js,ts,jsx,tsx,mdx}",
        "./pages/**/*.{js,ts,jsx,tsx,mdx}",
        "./components/**/*.{js,ts,jsx,tsx,mdx}",

        // Or if using `src` directory:
        "./src/**/*.{js,ts,jsx,tsx,mdx}",
        './node_modules/@eidolon-ai/**/*.js', // Your custom component library
    ],
    theme: {
        extend: {},
    },
    plugins: [],
    corePlugins: {
        preflight: false, // Disable Tailwind's reset to avoid conflicts with MUI
    }
}
