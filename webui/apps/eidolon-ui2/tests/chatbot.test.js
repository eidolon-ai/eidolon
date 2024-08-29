const { test, expect } = require('@playwright/test');

// Test to check if the chatbot responds to input
test('Chatbot should respond to input', async ({ page }) => {
    const chatInput = page.locator('textarea[aria-invalid="false"]');
    const submitInput = page.locator('button[id="submit-input-text"]')

    await page.goto('/eidolon-apps/sp/chatbot');
    await login(page);

    // Add a chat
    const addChatButton = page.getByText('Add Chat');
    await addChatButton.click();

    // Fill the input field with a message
    await chatInput.fill('Hello, how are you? Type "Hello!" if you are there!');
    await submitInput.click();
    const response = page.getByText("Hello!", { exact: true });

    await expect(response).toBeVisible();
    await expect(response).toContainText('Hello!');
});

async function login(page) {
    const emailField = page.locator('#input-username-for-credentials-provider');
    const randomEmail = `test${Math.random().toString(36).substring(7)}@example.com`;
    const eidolonDemoCloud = page.locator('text=Eidolon Demo Cloud');
    const login = page.locator('button[type="submit"]');

    if (await eidolonDemoCloud.isVisible()) {
        await emailField.fill(randomEmail);
        await login.click();
    }
}