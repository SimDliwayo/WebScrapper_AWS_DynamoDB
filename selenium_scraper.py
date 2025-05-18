from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from datetime import datetime
import time
import boto3

# Setup Edge Driver
edge_driver_path = "C:PATH//Please//Yes//edgeDRIVER.exe//PATH"
service = Service(executable_path=edge_driver_path)
options = webdriver.EdgeOptions()
driver = webdriver.Edge(service=service, options=options)

# Target URL
url = 'https://www.avo.africa/ecommerce/search/result-list?vertical=ESHOP&categoryId=WATER'
driver.get(url)


time.sleep(5)

# Get all product cards
product_cards = driver.find_elements(By.CSS_SELECTOR, 'a[ui-card-product]')

# Setup DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table("Avo_Water_Solution")  


count = 0
for card in product_cards:
    if count >= 10:
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
