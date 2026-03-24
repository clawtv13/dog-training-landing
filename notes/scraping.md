# SCRAPING — Scrapling Workflow

_Last updated: 2026-03-20_

---

## Tech Stack

**Library:** Scrapling (installed)  
**Alternative to:** requests + BeautifulSoup  
**GitHub:** https://github.com/D4Vinci/Scrapling

---

## Why Scrapling?

✅ Anti-bot evasion built-in  
✅ JavaScript rendering support  
✅ Proxy rotation  
✅ Cleaner API than BeautifulSoup  

---

## Basic Usage

### Simple Fetch

```python
from scrapling import Fetcher

# Create fetcher
fetcher = Fetcher()

# Fetch URL
page = fetcher.get("https://example.com")

# Extract text
title = page.css("h1::text").get()
items = page.css(".product::text").getall()
```

### With Anti-Bot Evasion

```python
# Enable stealth mode
fetcher = Fetcher(stealth=True, headless=True)

page = fetcher.get("https://example.com")
```

### With Proxy

```python
fetcher = Fetcher(
    proxy="http://your-proxy:8080",
    stealth=True
)
```

---

## Use Cases

### 1. Competitor Product Research

```python
from scrapling import Fetcher

def scrape_competitor_products(url):
    fetcher = Fetcher(stealth=True)
    page = fetcher.get(url)
    
    products = []
    for item in page.css(".product-card"):
        product = {
            "name": item.css(".product-name::text").get(),
            "price": item.css(".price::text").get(),
            "rating": item.css(".rating::text").get(),
            "url": item.css("a::attr(href)").get()
        }
        products.append(product)
    
    return products
```

### 2. Amazon Price Monitoring

```python
def monitor_amazon_price(asin):
    url = f"https://www.amazon.com/dp/{asin}"
    fetcher = Fetcher(stealth=True)
    page = fetcher.get(url)
    
    price = page.css(".a-price-whole::text").get()
    return price
```

### 3. Review Scraping

```python
def scrape_reviews(product_url):
    fetcher = Fetcher(stealth=True)
    page = fetcher.get(product_url)
    
    reviews = []
    for review in page.css(".review"):
        reviews.append({
            "author": review.css(".author::text").get(),
            "rating": review.css(".rating::attr(data-rating)").get(),
            "text": review.css(".review-text::text").get(),
            "date": review.css(".review-date::text").get()
        })
    
    return reviews
```

---

## Tips

### Rate Limiting

```python
import time

for url in urls:
    page = fetcher.get(url)
    # Process...
    time.sleep(2)  # Be nice to servers
```

### Error Handling

```python
from scrapling.exceptions import FetchError

try:
    page = fetcher.get(url)
except FetchError as e:
    print(f"Failed to fetch: {e}")
```

### Save to File

```python
import json

products = scrape_competitor_products(url)
with open("products.json", "w") as f:
    json.dump(products, f, indent=2)
```

---

## Pending Projects

- [ ] Competitor price tracker for LED masks
- [ ] Amazon review analyzer
- [ ] Trending product finder
- [ ] Shopify store analyzer
