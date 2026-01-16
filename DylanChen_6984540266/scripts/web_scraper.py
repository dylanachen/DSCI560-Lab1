"""
Author: Dylan Chen
USC ID: 6984540266
Date: 1/16/2026
Description: Web scraper for CNBC World News Page
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
import os
import time

# Define the URL to scrape
url = "https://www.cnbc.com/world/?region=world"
print(f"Web Scraping Target URL: {url}")

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)

        print("Waiting for market data to load...")
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, "market-data-scroll-container")))

        time.sleep(3)

        page_source = driver.page_source
        driver.quit()

except Exception as e:
        print(f"Error during scraping: {e}")
        driver.quit()
        exit(1)

'''
# Send GET request to site
try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        print(f"Retrieved page (Status Code: {response.status_code})")
except requests.exceptions.RequestException as e:
        print(f"Error fetching page: {e}")
        exit(1)
'''

# Parse HTML content
soup = BeautifulSoup(page_source, "html.parser")
print("HTML content parsed successfully")

# Getting path for data by going up one level from current directory
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(os.path.dirname(script_dir), "data", "raw_data")

# Ouputting data in HTML file
output_file = os.path.join(data_dir, "web_data.html")
with open(output_file, "w", encoding="utf-8") as f:
        f.write(soup.prettify())

# Print completion statement
print(f"HTML data saved to: {output_file}")
