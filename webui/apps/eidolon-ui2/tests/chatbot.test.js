const { test, expect } = require('@playwright/test');

// Test to check if the chatbot responds to input
test('Chatbot should respond to input', async ({ page }) => {
    await page.goto('/eidolon-apps/sp/chatbot');
    // If the user is not logged in, log in with a random email
    if (await page.locator('text=Eidolon Demo Cloud').isVisible()) {
        const randomEmail = `test${Math.random().toString(36).substring(7)}@example.com`;
        await page.fill('input[id="input-username-for-credentials-provider"]', randomEmail);
        await page.click('button[type="submit"]');
    }
    // Add a chat
    const addChatButton = await page.locator('text=Add Chat');
    await addChatButton.click();
    const inputField = await page.locator('textarea[aria-invalid="false"]');
    await inputField.waitFor();
    // Fill the input field with a message
    await inputField.fill('Hello, how are you? Type "Hello!" if you are there!');
    await page.locator('button[id="submit-input-text"]').click();
    const response = await page.getByText("Hello!", { exact: true });
    await response.waitFor();
    await expect(response).toBeVisible();
    await expect(response).toContainText('Hello!');
});
