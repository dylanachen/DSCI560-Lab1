"""
Author: Dylan Chen
USC ID: 6984540266
Date: 1/16/2026
Description: Parse web_data.html and extract market and news data to CSV files
"""

import os
import csv
from bs4 import BeautifulSoup

# Define paths
script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(script_dir)
raw_data_file = os.path.join(base_dir, 'data', 'raw_data', 'web_data.html')
processed_data_dir = os.path.join(base_dir, 'data', 'processed_data')

# Reading HTML data
#try:
#        with open(raw_data_file, 'r', encoding='utf-8') as f:
#                html_content = f.read()
#        print("Successfully read HTML file")
#except FileNotFoundError:
#        print(f"Error: {raw_data_file} not found")
#        exit(1)

# Parse HTML data
#soup = BeautifulSoup(html_content, 'html.parser')
#print("Parsed HTML content")

with open(raw_data_file, "r", encoding="utf-8") as f:
        html_lines = f.readlines()

soup = BeautifulSoup("".join(html_lines), "html.parser")

# Filtering Fields
print("Filtering Fields")

market_data = []
container = soup.find('div', id='market-data-scroll-container')
all_cards = container.find_all('a')
print(all_cards)
print(f"Found {len(all_cards)} total cards")

for card in all_cards:
        card_rows = card.find_all('div', class_='MarketCard-row')

        first_row = card_rows[0]
        second_row = card_rows[1]

        # Extract symbol
        symbol_elem = first_row.find('span', class_='MarketCard-symbol')
        symbol = symbol_elem.get_text(strip=True)
        print(f"Symbol: {symbol}")

        # Extract stock position
        price_elem = first_row.find('span', class_='MarketCard-stockPosition')
        stock_position = price_elem.get_text(strip=True)
        print(f"Position: {stock_position}")

        # Extract change percentage
        change_elem = second_row.find('span', class_='MarketCard-changesPct')
        change_pct = change_elem.get_text(strip=True)
        print(f"Change PCT: {change_pct}")

        # Appending market data
        market_data.append({
                'symbol': symbol,
                'stock_position': stock_position,
                'change_pct': change_pct
        })


# Extracting News Data
news_data = []
news_list = soup.find('ul', class_='LatestNews-list')

if news_list:
        # Find all news items
        news_items = news_list.find_all('li', class_='LatestNews-item')

        for item in news_items:
                try:
                        # Extract timestamp
                        timestamp_elem = item.find('time', class_='LatestNews-timestamp')
                        timestamp = timestamp_elem.get_text(strip=True)

                        # Extract title and link
                        headline_elem = item.find('a', class_='LatestNews-headline')
                        title = headline_elem.get_text(strip=True)
                        link = headline_elem['href']

                        # Appending news data
                        news_data.append({
                                'timestamp': timestamp,
                                'title': title,
                                'link': link
                        })

                except Exception as e:
                        print(f"Error Processing News Items: {e}")
                        continue

print("\nFields Filtered")

# Saving to CSVs

market_csv_path = os.path.join(processed_data_dir, 'market_data.csv')
with open(market_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['symbol', 'stock_position', 'change_pct']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(market_data)

news_csv_path = os.path.join(processed_data_dir, 'news_data.csv')
with open(news_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['timestamp', 'title', 'link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(news_data)

print("Fields saved to CSV")
