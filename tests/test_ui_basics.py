""" this file contains test cases for basic UI testing with Playwright """
import pytest
from playwright.sync_api import Page, expect, Browser

@pytest.mark.skip
def test_ui(page: Page, init_logger):
    logger = init_logger

    # selectors and locators
    userName = page.locator('#username')  # id attribute
    signIn = page.locator('#signInBtn')   # id attribute
    cardTitle = page.locator('.card-body a')  # classname attribute
    password = page.locator("[type='password']")  # use attribute name and value directly
    errorMsg = page.locator("[style*='block']")   # can also use partial attribute value (instead of [style='display: block'])

    page.goto("https://rahulshettyacademy.com/loginpagePractise/")
    logger.info(f"page title = {page.title()}")

    userName.fill("rahulshetty")
    password.fill("learning")
    signIn.click()
    logger.info(f"{errorMsg.text_content()}")
    expect(errorMsg).to_contain_text('Incorrect')

    userName.fill("")
    userName.fill("rahulshettyacademy")
    password.fill("learning")
    signIn.click()
    #logger.info(f"first card title: {page.locator('.card-body a').first.text_content()}")
    #logger.info(f"second card title: {page.locator('.card-body a').nth(1).text_content()}")
    cardTitle.first.wait_for()  # needed because all_text_contents() does not auto-wait
    allTitles = cardTitle.all_text_contents()
    logger.info(f"card titles are: {allTitles}")


def test_ui_controls(page: Page, init_logger):
    logger = init_logger

    page.goto("https://rahulshettyacademy.com/loginpagePractise/")
    userName = page.locator('#username')
    signIn = page.locator('#signInBtn')
    password = page.locator("[type='password']")
    dropdown = page.locator(("select.form-control"))

    dropdown.select_option("consult")
    page.locator(".radiotextsty").last.click()
    page.locator("#okayBtn").click()
    logger.info(f"button s clicked?: {page.locator(".radiotextsty").last.is_checked()}")
    expect(page.locator(".radiotextsty").last).to_be_checked()
    page.locator("#terms").click()
    expect(page.locator("#terms")).to_be_checked()
    page.locator("#terms").uncheck()
    expect(page.locator("#terms")).not_to_be_checked()

    #page.pause()

@pytest.mark.skip
def test_child_windows(browser: Browser, init_logger):
    logger = init_logger

    # set up a browser context and then create a page
    context = browser.new_context()
    page = context.new_page()

    # set up locator
    userName = page.locator('#username')
    signIn = page.locator('#signInBtn')
    password = page.locator("[type='password']")

    page.goto("https://rahulshettyacademy.com/loginpagePractise/")

    userName.fill("")
    userName.fill("rahulshettyacademy")
    password.fill("learning")
    signIn.click()

    with context.expect_page() as new_page:
        page.locator("[href*='documents-request']").click()
    docs_page = new_page.value
    text = docs_page.locator(".red").text_content()
    logger.info(f"here's the text from the Docs page: {text}")

