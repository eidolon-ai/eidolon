import { defineConfig } from 'tsup';

export default defineConfig([
    {
        entry: {
            index: './src/client/index.ts',
        },
        outDir: 'dist/client',
        format: ['esm', 'cjs'],
        dts: true,
        sourcemap: true,
        minify: true,
        external: ['react'],
        esbuildOptions(options) {
            options.banner = {
                js: '"use client"',
            };
        },
    },
    {
        entry: {
            index: './src/server/index.ts',
        },
        outDir: 'dist/server',
        format: ['esm', 'cjs'],
        dts: true,
        sourcemap: true,
        minify: true,
        external: ['react'],
        esbuildOptions(options) {
            options.banner = {
                js: '"use server"',
            };
        },
    },
]);