import os
import time
import requests
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service

load_dotenv()

router_url = os.getenv('ROUTER_URL')
login_password = os.getenv('ROUTER_PASSWORD')

def has_internet():
    """Check if the computer has internet access."""
    try:
        # Try to reach google.com
        requests.get("https://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False

def reboot_router(driver, router_url, login_password):
    try:
        # Navigate to the login page
        driver.get(router_url)

        # Wait for the login input box to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[2]/div/ul/li/input"))
        )

        # Enter the login password
        login_input = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div/ul/li/input")
        login_input.send_keys(login_password)

        # Click the login button
        login_button = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div/label")
        login_button.click()

        # Wait for the next page to load and ensure login is successful
        time.sleep(5)  # Adjust this based on the speed of your network and router

        driver.switch_to.frame("frame1")

        system_tools = driver.find_element(By.XPATH, "/html/body/div/div[1]/ul/li[17]/a")
        system_tools.click()

        time.sleep(2)

        reboot = driver.find_element(By.XPATH, "/html/body/div/div[1]/ul/li[17]/ul/li[7]/a")
        reboot.click()

        time.sleep(2)

        # Switch back to the main frame
        driver.switch_to.default_content()
        driver.switch_to.frame("frame2")

        prompt_message = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/p[1]")
        print(prompt_message.text)

        # Uncomment these lines to perform the actual reboot
        # Click the reboot button
        # reboot_button = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/p[3]/input")
        # reboot_button.click()

        # Choose yes on the alert that pops up
        # alert = driver.switch_to.alert
        # alert.accept()

        # print("Rebooting the router...")

        time.sleep(5)
    finally:
        # Close the web driver
        driver.quit()

# Set up Chrome options for headless mode
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Initialize Chrome WebDriver with the path to chromedriver and headless options
service = Service(executable_path="/usr/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=options)

# Check internet connectivity and reboot router if no internet
if not has_internet():
    print("No internet connection. Rebooting the router...")
    #reboot_router(driver, router_url, login_password)
else:
    print("Internet connection is available.")
