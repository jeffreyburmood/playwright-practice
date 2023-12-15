""" this file contains test cases for basic UI testing with Playwright """

from playwright.sync_api import Page, expect, Browser

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

    # userName.fill("rahulshetty")
    # password.fill("learning")
    # signIn.click()
    # logger.info(f"{errorMsg.text_content()}")
    # expect(errorMsg).to_contain_text('Incorrect')

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

def test_child_windows(browser: Browser, init_logger):
    logger = init_logger

    context = browser.new_context()
    page = context.new_page()

    page.goto("https://rahulshettyacademy.com/loginpagePractise/")
    documentLink = page.locator("[href+='documents-request']")
    documentLink.click()
    page2 = context.wait_for_event() # listen for any new page

