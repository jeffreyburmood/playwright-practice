""" this file contains test cases for E2E client app testing with Playwright """
import pytest
from playwright.sync_api import Page, expect, Browser

def test_client(page: Page, init_logger):
    logger = init_logger

    email = "anshika@gmail.com"
    # selectors and locators
    userLogin = page.locator("#userEmail")
    userPassword = page.locator("#userPassword")
    loginButton = page.locator("[value='Login']")
    products = page.locator(".card-body")

    # log into client retail site
    page.goto("https://rahulshettyacademy.com/client")
    userLogin.fill(email)
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
    # assert that the desired product is on the page
    expect(page.locator("h3:has-text('ZARA COAT 3')")).to_be_visible()
    # now click on the checkout button
    page.locator("text=Checkout").click()

    # now work through the checkout page filling in the required information
    # personal information
    # credit card
    page.locator("input[type='text']").first.fill("4278 9999 0000 0000")
    page.get_by_role("combobox").first.select_option('02')
    page.get_by_role("combobox").last.select_option('25')
    page.locator("input[type='text']").nth(1).fill("234")
    page.locator("input[type='text']").nth(2).fill("John Smith")
    #page.locator("input[name='coupon']").fill("COUPON")
    #page.get_by_role("button", name="Apply Coupon").click()
    # shipping information
    # select country for shipping by slowly typing first few letters
    page.locator("[placeholder*='Country']").press_sequentially("ind")
    dropdown = page.locator(".ta-results")
    dropdown.wait_for()
    options_count = dropdown.locator("button").count()
    for i in range(0, options_count):
        text = dropdown.locator("button").nth(i).text_content()
        if text.lstrip() == "India":
            dropdown.locator("button").nth(i).click()
            break

    logger.info(f"Completed entering checkout information")

    # place the order
    # confirm the correct email
    expect(page.locator(".user__name [type='text']").first).to_contain_text(email)
    # place the order
    page.locator("a:has-text('Place Order')").click()
    logger.info(f"order has been placed")
    # verify the order was placed successfully
    expect(page.locator(".hero-primary")).to_contain_text(" Thankyou for the order. ")
    # grab the order ID to print out
    order_id = page.locator(".em-spacer-1 .ng-star-inserted").text_content()
    logger.info(f"the Order ID = ${order_id}")

    # verify the order appears on the Orders page
    page.locator("button[routerlink*='myorders']").click()
    # grab the table with all of the orders
    # wait for table body to load so the count() method will work
    page.locator("tbody").wait_for()
    rows = page.locator("tbody tr")
    logger.info(f"orders row count = {rows.count()}")
    # loop through each row of the table and check the order ID
    for i in range(0, rows.count()):
        row_orderID = rows.nth(i).locator("th").text_content()
        logger.info(f"row order id = {row_orderID}")
        if order_id.find(row_orderID) != -1:
            rows.nth(i).locator("button").first.click()
            break

    # we're now viewing the order summary
    logger.info(f"we're now viewing the order summary")

    # verify the order id on the order summary page
    order_details = page.locator(".col-text").text_content()
    logger.info(f"here are the order details {order_details}")
