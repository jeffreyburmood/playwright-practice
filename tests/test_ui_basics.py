""" this file contains test cases for basic UI testing with Playwright """

from playwright.sync_api import Page, expect

def test_ui(page: Page, init_logger):
    logger = init_logger

    # selectors and locators
    userName = page.locator('#username')
    signIn = page.locator('#signInBtn')
    cardTitle = page.locator('.card-body a')
    password = page.locator("[type='password']")
    errorMsg = page.locator("[style*='block']")

    page.goto("https://rahulshettyacademy.com/loginpagePractise/")
    logger.info(f"page title = {page.title()}")

    userName.fill("rahulshetty")
    password.fill("learning")
    signIn.click()
    logger.info(f"{errorMsg.text_content()}")
    expect(errorMsg).to_contain_text('Incorrect')
