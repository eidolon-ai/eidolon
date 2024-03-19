const {resolve} = require("node:path");

const project = resolve(process.cwd(), "tsconfig.json");

/*
 * This is a custom ESLint configuration for use with
 * internal (bundled by their consumer) libraries
 * that utilize React.
 *
 * This config extends the Vercel Engineering Style Guide.
 * For more information, see https://github.com/vercel/style-guide
 *
 */

/** @type {import("eslint").Linter.Config} */
module.exports = {
    extends: ["eslint:recommended", "prettier", "eslint-config-turbo"],
    plugins: ["only-warn"],
    globals: {
        React: true,
        JSX: true,
    },
    env: {
        browser: true,
    },
    settings: {
        "import/resolver": {
            typescript: {
                project,
            },
        },
    },
    rules: {
        'no-unused-vars': [
            'warn',
            {
                argsIgnorePattern: '^_',
                varsIgnorePattern: '^_',
            },
        ],
    },
    ignorePatterns: [
        // Ignore dotfiles
        ".*.js",
        "index.ts",
        "jest.config.ts",
        "node_modules/",
        "dist/",
        "test/",
        "coverage/"
    ],
    overrides: [
        // Force ESLint to detect .tsx files
        {files: ["*.js?(x)", "*.ts?(x)"]},
    ],
};
