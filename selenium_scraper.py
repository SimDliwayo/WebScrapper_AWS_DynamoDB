from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from datetime import datetime
import time
import boto3
import json
import os


#Load some configs 
with open('.config/config.json', 'r') as f:
    config = json.load(f)

driver_path_file = config['driver_path_file']
with open(driver_path_file, 'r') as f:
    edge_driver_path = f.read().strip()


# Setup Edge Driver
service = Service(executable_path=edge_driver_path)
options = webdriver.EdgeOptions()
driver = webdriver.Edge(service=service, options=options)

# Target URL
driver.get(config['target_url'])

time.sleep(config['sleep_time'])

# Get all product cards
product_cards = driver.find_elements(By.CSS_SELECTOR, 'a[ui-card-product]')

# Setup DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table("Avo_Water_Solution")  


count = 0
for card in product_cards:
    if count >= 3:
        break

    try:
        title = card.find_element(By.CSS_SELECTOR, 'p.text-h5').text.strip()

        price = card.find_element(By.CSS_SELECTOR, 'div.text-h4').text.strip()

        # Extract Greenbacks price
        try:
            greenbacks_price = card.find_element(By.CSS_SELECTOR, 'div.text-primary-good-green').text.strip()
        except:
            greenbacks_price = "N/A"

        print(f"Title: {title}")
        print(f"Price: {price}")
        print(f"Greenbacks Price: {greenbacks_price}")

        # Save to DynamoDB
        product_id = str(hash(title + price))
        table.put_item(
            Item={
                'product_id': product_id,
                'Product_title': title,
                'Price': price,
                'Greenbacks_price': greenbacks_price,
                'Scraped_at': str(datetime.now())
            }
        )

        count += 1

    except Exception as e:
        print(f"Failed to process a product card: {e}")

driver.quit()
print("Products have been scraped and stored in DynamoDB.")
