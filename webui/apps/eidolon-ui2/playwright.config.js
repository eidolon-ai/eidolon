const { defineConfig, devices } = require('@playwright/test');

module.exports = defineConfig({
    testDir: './tests',
    outputDir: 'tests/test-results',
    timeout: 30000,
    retries: 2,
    use: {
        headless: true,
        baseURL: 'http://localhost:3000',
        screenshot: 'only-on-failure',
    },
    projects: [
        {
            name: 'chromium',
            use: { ...devices['Desktop Chrome'] },
        },
        // TODO: Get Safari working
        // {
        //     name: 'safari',
        //     use: { ...devices['Desktop Safari'] },
        // },
        {
            name: 'firefox',
            use: { ...devices['Desktop Firefox'] },
        },
    ],
    webServer: {
        command: 'pnpm docker compose up',
        cwd: '../../..',
        port: 3000,
        timeout: 120000,
        reuseExistingServer: true,
    },
});
