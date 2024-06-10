const { defineConfig } = require('@playwright/test');

module.exports = defineConfig({
    testDir: './tests',
    timeout: 30000,
    retries: 2,
    use: {
        headless: true,
        baseURL: 'http://localhost:3000',
        screenshot: 'only-on-failure',
    },
    webServer: {
        command: 'pnpm docker-compose up',
        cwd: '../../..',
        port: 3000,
        timeout: 120000,
        reuseExistingServer: true,
    },
});
