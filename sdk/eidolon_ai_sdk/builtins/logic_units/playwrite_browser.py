from typing import Any


class PlaywrightWrapper:
    """Wrapper around Playwright.

    To use this wrapper, you must have Playwright installed and the `playwright`
    python package installed.
    """

    def __init__(
        self,
        playwright_browser_type: str = "chromium",
        timeout: int = 5000,
        **kwargs: Any,
    ) -> None:
        """Initialize the PlaywrightWrapper.

        Args:
            playwright_browser_type: The type of browser to use.
            timeout: The timeout to use when launching the browser.
            kwargs: Additional arguments to pass to the browser.
        """
        try:
            import playwright
        except ImportError:
            raise ImportError("playwright is not installed. Please install it with `pip install playwright`.")
        self.playwright = playwright
        self.playwright_browser_type = playwright_browser_type
        self.timeout = timeout
        self.kwargs = kwargs

    def _create_browser_context(self, **kwargs: Any) -> Any:
        browser = (
            self.playwright.sync_playwright()
            .start()
            .launcher.launch(self.playwright[self.playwright_browser_type], **kwargs)
        )
        return browser.new_context()

    def run(self, url: str) -> str:
        """Run the specified URL and return the HTML.

        Args:
            url: The URL to run.

        Returns:
            The HTML of the page.
        """
        context = self._create_browser_context()
        page = context.new_page()
        try:
            page.goto(url, timeout=self.timeout)
            return page.content()
        finally:
            context.close()
            self.playwright.stop()

    def cleanup(self) -> None:
        """Clean up the Playwright instance."""
        self.playwright.stop()
