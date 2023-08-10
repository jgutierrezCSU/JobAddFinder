from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Configure Chrome options for headless browsing
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Set path to chromedriver executable as per your configuration
chromedriver_path = "./chromedriver"

# Set Chrome options and initialize the driver
driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)

# URL to scrape
url = "https://example.com"

# Perform scraping
driver.get(url)

# Extract desired information from the webpage
title = driver.title
content = driver.page_source

# Print the results
print("Page Title: ", title)
print("Page Content: ", content)

# Close the browser
driver.quit()