
from selenium import webdriver
from selenium.webdriver.common.by import By 
from datetime import datetime 
import time
import boto3

# import Quotes_Scrapper

# Set the path to your Edge WebDriver
edge_driver_path = "C:your/driver/path" # Yes you! who's reading this code;)

# Initialize Edge WebDriver
options = webdriver.EdgeOptions()
driver = webdriver.Edge(options=options)

# Open the website
url = 'http://quotes.toscrape.com/js/'
driver.get(url)


# Wait for JavaScript to load
time.sleep(3)

# Find all quotes on the page
quotes_elements = driver.find_elements(By.CLASS_NAME, 'quote')


# Initialize DynamoDB resource 
# table = Quotes_Scrapper.initialize_table('QuotesTable')
dynamodb = boto3.resource('dynamodb', region_name='us-east-1') 
table = dynamodb.Table("QuotesTable")

# Extract and store data
for quote_element in quotes_elements:
    text = quote_element.find_element(By.CLASS_NAME, 'text').text
    author = quote_element.find_element(By.CLASS_NAME, 'author').text
    tags = [tag.text for tag in quote_element.find_elements(By.CLASS_NAME, 'tag')]

    # Create a unique Quote ID
    quote_id = str(hash(text))
    # Save data to DynamoDB
    table.put_item(
        Item={
            'Quote_id': quote_id,
            'Author_name': author,
            'Quote_text': text,
            'Tags': ", ".join(tags),
            'Scraped_at': str(datetime.now())
        }
    )
print("Quotes have been scraped and stored in DynamoDB using Selenium.")

# Close the browser
driver.quit()
