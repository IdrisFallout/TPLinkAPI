import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# Configuration
router_url = os.getenv("ROUTER_URL", "http://192.168.0.1")
login_password = os.getenv("ROUTER_PASSWORD", "admin")

# Try to initialize the web driver for Chrome
driver = None

try:
    # Try Chrome
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
except Exception as e:
    print(f"Chrome not available: {e}")

if driver is None:
    print("No supported browser found on the system.")
    exit(1)

try:
    # Navigate to the login page
    driver.get(router_url)

    # Wait for the login input box to be present
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[2]/div/ul/li/input")))

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

    # switch back to the main frame
    driver.switch_to.default_content()
    driver.switch_to.frame("frame2")

    # Click the reboot button /html/body/div[1]/div/div/div[1]/p[3]/input
    reboot_button = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/p[3]/input")
    reboot_button.click()

    # Choose yes on the alert that pops up
    alert = driver.switch_to.alert
    alert.accept()

    print("Rebooting the router...")

    time.sleep(5)

finally:
    # Close the web driver
    driver.quit()
