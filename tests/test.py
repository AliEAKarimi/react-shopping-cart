# a test with selenium for the typescript-react-shopping-cart project

import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class TypescriptReactShoppingCartTest(unittest.TestCase):
    def setUp(self):
      # create a new Chrome session
      self.driver = webdriver.Chrome()
      # maximize the window size
      self.driver.maximize_window()
      # delete all cookies
      self.driver.delete_all_cookies()
      # navigate to the application home page
      self.driver.get("http://localhost:3000")
      # self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
      # close the browser window
      self.driver.quit()

    # 1. Title test: Verify that the title of the page is correct
    def test_title(self):
      time.sleep(2)
      self.title = self.driver.title
      self.assertEqual(self.title, "Typescript React Shopping cart")


    # 2. Product test: Verify that the products are displayed correctly
    def test_display_16_products_correctly(self):
      time.sleep(2)
      # Find all product cards on the page
      self.product_cards = self.driver.find_elements(By.XPATH, "//*[contains(@class, 'product-card')]")
      # Verify that there are 16 products on the page
      assert len(self.product_cards) == 16
      # Verify that each product card has an image, title, price and add to cart button
      for product_card in self.product_cards:
          assert product_card.find_element(By.XPATH, "//*[contains(@id, 'product-image')]")
          assert product_card.find_element(By.XPATH, "//*[contains(@id, 'product-title')]")
          assert product_card.find_element(By.XPATH, "//*[contains(@id, 'product-price')]")
          assert product_card.find_element(By.XPATH, "//*[contains(@id, 'add-to-cart-button')]")

    # 3. Empty cart test: Verify that the cart is empty when the page is loaded
    def test_empty_cart(self):
        time.sleep(2)
        # Find the cart icon
        cart_quantity = self.driver.find_element(By.XPATH, "//*[contains(@id, 'cart-quantity')]")
        self.assertEqual(cart_quantity.text, '0')

    # 4. Add to cart test: Verify that the product is added to the cart
    def test_add_product_to_cart(self):
        # Find the first product card on the page
        product_card = self.driver.find_element(
          By.XPATH, "//*[contains(@class, 'product-card')]"
        )
        # Click the Add to Cart button
        product_card.find_element(
          By.XPATH, "//*[contains(@id, 'add-to-cart-button')]"
        ).click()
        time.sleep(2)
        # Close the cart modal
        cartButton = self.driver.find_element(By.XPATH, "//*[@id=\"open-cart-button\"]")
        cartButton.click()
        time.sleep(2)
        # Verify that the cart icon shows 1 item
        cart_quantity = self.driver.find_element(By.XPATH, "//*[contains(@id, 'cart-quantity')]")
        assert cart_quantity.text == '1'

    # 5. Filter by size test: Verify that the products are filtered by size
    def test_filter_products_by_size(self):
      checkbox = self.driver.find_element(By.XPATH, "//*[contains(@id, 'XXL')]")
      checkbox.click()
      time.sleep(2)
      product_cards = self.driver.find_elements(By.XPATH, "//*[contains(@class, 'product-card')]")
      assert len(product_cards) == 4

    # 6. Cart list test: Verify that the cart list displays all products added to the cart
    def test_cart_list(self):
       # Find the first product card on the page
        product_card = self.driver.find_element(
          By.XPATH, "//*[contains(@class, 'product-card')]"
        )
        productName = product_card.find_element(By.XPATH, "//*[contains(@id, 'product-title')]").text
        productPrice = product_card.find_element(By.XPATH, "//*[contains(@id, 'product-price')]").text
        # Click the Add to Cart button
        product_card.find_element(
          By.XPATH, "//*[contains(@id, 'add-to-cart-button')]"
        ).click()
        time.sleep(2)
        # Verify that the cart list displays the product added to the cart
        # cartProducts = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[contains(@class, 'cart-product')]")))
        cartProducts = self.driver.find_elements(By.XPATH, "//*[contains(@class, 'cart-product')]")
        assert len(cartProducts) == 1
        # Verify that the product name is displayed correctly
        cartProductName = cartProducts[0].find_element(By.XPATH, "//*[contains(@id, 'cart-product-title')]").text
        assert productName == cartProductName
        # Verify that the product price is displayed correctly
        cartProductPrice = cartProducts[0].find_element(By.XPATH, "//*[contains(@id, 'cart-product-price')]").text
        assert cartProductPrice.replace(" ", "") == productPrice.split("\n")[0]
        # Verify Remove button works
        cartProducts[0].find_element(By.XPATH, "//*[contains(@id, 'remove-product')]").click()
        time.sleep(2)


    # 7. Checkout test: Verify that the checkout button displays an alert message when the cart is empty
    def test_checkout_button_alert_message(self):
        # Click the cart button
        cartButton = self.driver.find_element(By.XPATH, "//*[contains(@id, 'open-cart-button')]")
        cartButton.click()
        time.sleep(2)
        # Click the checkout button
        checkoutButton = self.driver.find_element(By.XPATH, "//*[contains(@id, 'checkout-button')]")
        checkoutButton.click()
        time.sleep(2)
        # Verify that an alert message is displayed
        alert = self.driver.switch_to.alert
        assert alert.text == 'Add some product in the cart!'
        time.sleep(2)

    # 8. Link test: Verify that the link to the github star page is working
    def test_github_link(self):
        # Click the github link
        githubLink = self.driver.find_element(By.XPATH, "//*[contains(@id, 'github-star-link')]")
        githubLink.click()
        time.sleep(2)
        # Verify that the github page is displayed
        assert self.driver.current_url == 'https://github.com/jeffersonRibeiro/react-shopping-cart'
        
if __name__ == "__main__":
  unittest.main()
