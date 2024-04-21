""" Explore Playwright special locators """
from playwright.sync_api import Page, expect, sync_playwright, Playwright

def test_getby_locators(page: Page, init_logger):
    logger = init_logger

    page.goto("https://rahulshettyacademy.com/angularpractice/")

    page.get_by_label("Check me out if you Love IceCreams!").click()

    page.get_by_label("Employed").check()

    page.get_by_label("Gender").select_option("Female")

    page.get_by_placeholder("Password").fill("password")

    page.get_by_role("button", name = 'Submit').click()

    page.get_by_text("The Form has been submitted successfully!").is_visible()

    page.get_by_role("link", name='Shop').click()

    page.locator("app-card").filter(has_text='Nokia Edge').get_by_role("button").click()
