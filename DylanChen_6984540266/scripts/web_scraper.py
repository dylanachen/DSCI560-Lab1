"""
Author: Dylan Chen
USC ID: 6984540266
Date: 1/16/2026
Description: Web scraper for CNBC World News Page
"""

import requests
from bs4 import BeautifulSoup
import os

# Define the URL to scrape
url = "https://www.cnbc.com/world/?region=world"
print(f"Web Scraping Target URL: {url}")

# Send GET request to site
try:
	response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
	response.raise_for_status()  # Raise an error for bad status codes
	print(f"Retrieved page (Status Code: {response.status_code})")
except requests.exceptions.RequestException as e:
	print(f"Error fetching page: {e}")
	exit(1)

# Parse HTML content
soup = BeautifulSoup(response.content, 'html.parser')
print("HTML content parsed successfully")

# Getting path for data by going up one level from current directory
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(os.path.dirname(script_dir), 'data', 'raw_data')

# Ouputting data in HTML file
output_file = os.path.join(data_dir, 'web_data.html')
with open(output_file, 'w', encoding='utf-8') as f:
	f.write(soup.prettify())

# Print completion statement
print(f"HTML data saved to: {output_file}")
