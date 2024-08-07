# Importing required libraries

# pip install selenium

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

# Setting up the webdriver
driver = webdriver.Chrome()

# Navigating to the Amazon.ca homepage
driver.get("https://www.amazon.ca")
time.sleep(8)

# Finding the search bar and entering text
# search_bar = driver.find_element_by_id("id","twotabsearchtextbox") old syntax
search_bar = driver.find_element(By.ID, "twotabsearchtextbox")
search_bar.send_keys("laptop")

# Submitting the search query
search_bar.send_keys(Keys.RETURN)

# Waiting for the search results page to load
time.sleep(5)

# Verifying that the search results page has loaded
assert "laptop" in driver.title

# Selecting a laptop from the search results
laptop_link = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[1]/div[1]/div/span[1]/div[1]/div[3]/div/div/div/div/span/div/div/div[1]/span/a/div/img")
laptop_link.click()

# Waiting for the laptop details page to load
time.sleep(2)

# Adding the laptop to the cart
add_to_cart_button = driver.find_element(By.ID, "add-to-cart-button")
add_to_cart_button.click()

# Waiting for the cart to update
time.sleep(5)

# clicking on "no thanks" button
no_thanks_button = driver.find_element(By.XPATH, "//*[@id=\"attachSiNoCoverage\"]/span/input")

# if "no thanks" button were not present, skip it
if (no_thanks_button):
    no_thanks_button.click()
    time.sleep(2)

# proceed_to_checkout
proceed_to_checkout= driver.find_element(By.NAME, "proceedToRetailCheckout")
proceed_to_checkout.click()

# waiting for sign-in form to load
time.sleep(4)

# Submitting the email
email_input = driver.find_element(By.ID, "ap_email")
email_input.send_keys("brian.class@gmail.com")
email_input.send_keys(Keys.RETURN)

# waiting for password form to load and to be manually filled
time.sleep(10)

# clicking the sig-in button
sigin_button = driver.find_element(By.ID, "signInSubmit")
sigin_button.click()

# waiting for OTP form to load and to be manually filled
time.sleep(10)

# Verifying that the laptop has been added to the cart
# cart_count = driver.find_element("id","nav-cart-count")
# assert cart_count.text == "1"
# cart_count.click()

# Closing the webdriver
driver.close()
