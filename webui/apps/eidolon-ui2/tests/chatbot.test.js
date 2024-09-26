const { test, expect } = require('@playwright/test');

// Test to check if the chatbot responds to input
test('Chatbot should respond to input', async ({ page }) => {
    await page.goto('/eidolon-apps/sp/chatbot');

    const chatInput = page.locator('#chat-input div[contenteditable="true"]');
    const submitInput = page.locator('#submit-chat')

    // Fill the input field with a message
    await chatInput.fill('Hello, how are you? Type "Hello!" if you are there!');
    await submitInput.click();
    const response = page.getByText("Hello!", { exact: true });

    await expect(response).toBeVisible();
    await expect(response).toContainText('Hello!');
});
