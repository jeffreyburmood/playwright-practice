import re
from playwright.sync_api import Page, expect, sync_playwright, Playwright

def test_has_title(page: Page):
    page.goto("https://playwright.dev/")

    # Expect a title "to contain" a substring.
    expect(page).to_have_title(re.compile("Playwright"))

#
# default browser context
#
def test_get_started_link(page: Page):
    page.goto("https://playwright.dev/")

    # Click the get started link.
    page.get_by_role("link", name="Get started").click()

    # Expects page to have a heading with the name of Installation.
    expect(page.get_by_role("heading", name="Installation")).to_be_visible()

def test_browser_context_approach(playwright: Playwright):
    webkit = playwright.webkit
    browser = webkit.launch(headless=True)
    # create a new incognito browser context
    context = browser.new_context()
    # create a new page inside context.
    page = context.new_page()
    page.goto("https://example.com")
    # dispose context once it is no longer needed.
    context.close()