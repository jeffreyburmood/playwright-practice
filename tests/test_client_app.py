""" this file contains test cases for E2E client app testing with Playwright """
import pytest
from playwright.sync_api import Page, expect, Browser

def test_client_app(page: Page, init_logger):
    logger = init_logger

    # selectors and locators
    userLogin = page.locator("#userEmail")
    userPassword = page.locator("#userPassword")
    loginButton = page.locator("[value='Login']")
    products = page.locator(".card-body")

    # log into client retail site
    page.goto("https://rahulshettyacademy.com/client")
    userLogin.fill("anshika@gmail.com")
    userPassword.fill("Iamking@000")
    loginButton.click()

    # get list of products
    product_name = "ZARA COAT 3"
    products.first.wait_for()  # needed because all_text_contents() does not auto-wait
    logger.info(f"products list size = {products.count()}")
    for i in range(0, products.count()):
        if products.nth(i).locator("b").text_content() == product_name:
            products.nth(i).locator("text= Add To Cart").click()
            break

    # check that selected product item has been added to the cart
    # go to cart page (look for tagname of "routerlink")
    page.locator("[routerlink*='cart']").click()
    # wait for the list of products to load
    page.locator("div li").first.wait_for()
    # find out if the desired product is on the page
    expect(page.locator("h3:has-text('ZARA COAT 3')")).to_be_visible()



