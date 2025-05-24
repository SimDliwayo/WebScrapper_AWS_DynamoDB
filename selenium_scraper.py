import os
import json
import time
from datetime import datetime
import boto3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service

# === Configuration ===
def load_config():
    with open('.config/config.json', 'r') as f:
        return json.load(f)

def get_driver_path(path_file):
    with open(path_file, 'r') as f:
        return f.read().strip()

# === Setup ===
def setup_driver(edge_driver_path):
    service = Service(executable_path=edge_driver_path)
    options = webdriver.EdgeOptions()
    driver = webdriver.Edge(service=service, options=options)
    return driver

def setup_dynamodb(table_name):

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table(table_name)

    return table

# === Scraping ===
def extract_product_data(card):
    try:
        title = card.find_element(By.CSS_SELECTOR, 'p.text-h5').text.strip()
        price = card.find_element(By.CSS_SELECTOR, 'div.text-h4').text.strip()
        try:
            greenbacks_price = card.find_element(By.CSS_SELECTOR, 'div.text-primary-good-green').text.strip()
        except:
            greenbacks_price = "N/A"
        return {
            'title': title,
            'price': price,
            'greenbacks_price': greenbacks_price
        }
    except Exception as e:
        print(f"Failed to extract product data: {e}")
        return None

def scrape_products(driver, table, target_url, sleep_time, max_products):
    driver.get(target_url)
    time.sleep(sleep_time)
    
    product_cards = driver.find_elements(By.CSS_SELECTOR, 'a[ui-card-product]')
    
    count = 0
    for card in product_cards:
        if count >= max_products:
            break

        product = extract_product_data(card)
        if product:
            print(f"Title: {product['title']}")
            print(f"Price: {product['price']}")
            print(f"Greenbacks Price: {product['greenbacks_price']}")

            product_id = str(hash(product['title'] + product['price']))
            table.put_item(
                Item={
                    'product_id': product_id,
                    'Product_title': product['title'],
                    'Price': product['price'],
                    'Greenbacks_price': product['greenbacks_price'],
                    'Scraped_at': str(datetime.now())
                }
            )
            count += 1

# === Main Execution ===
def main():
    config = load_config()
    driver_path = get_driver_path(config['driver_path_file'])

    driver = setup_driver(driver_path)
    table = setup_dynamodb("Avo_Water_Solution")

    try:
        scrape_products(
            driver,
            table,
            config['target_url'],
            config['sleep_time'],
            config['max_products']
        )
    finally:
        driver.quit()
        print("Products have been scraped and stored in DynamoDB.")

if __name__ == "__main__":
    main()
