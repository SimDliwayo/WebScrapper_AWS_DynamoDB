# 🛒 Avo Water Product Scraper

This project scrapes product data (titles, prices, and Greenbacks prices) from the Avo by Nedbank platform using Selenium and uploads the results to AWS DynamoDB.

---

## 📌 Features

- Uses **Microsoft Edge WebDriver** for scraping.
- Extracts product title, price, and loyalty (Greenbacks) pricing.
- Dynamically configurable via `.config/config.json`.
- Stores results in a **DynamoDB** table (`Avo_Water_Solution`).
- Handles internal proxy setup if required.
- Automatically limits number of products processed based on configuration.

---

---

## ⚙️ Configuration

Edit `.config/config.json`:

```json
{
  "driver_path_file": ".config/edge_driver_path.txt",
  "target_url": "https://avo.africa.example.com/water-solutions",
  "sleep_time": 3,
  "max_products": 10
}
```
---

## How to Run ⚙️

- Run `python selenuim_scrapper.py`

