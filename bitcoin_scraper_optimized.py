from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
import pandas as pd
from datetime import datetime

# --- Setup Chrome Options ---
options = Options()
options.add_argument("--headless")           # Run in headless mode (faster)
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Random User-Agent for stealth
options.add_argument(f"user-agent={UserAgent().random}")

# Initialize ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
URL = "https://coinmarketcap.com/currencies/bitcoin/"

# --- Scraper Function ---
def scrape_bitcoin_data():
    """Scrape Bitcoin market data from CoinMarketCap efficiently."""
    driver.get(URL)

    try:
        wait = WebDriverWait(driver, 10)
        # Shorter and faster XPaths (rely on simpler structure & stable attributes)
        price = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span[data-test="text-cdp-price-display"]'))).text
        market_cap = driver.find_element(By.XPATH, "//div[text()='Market cap']/ancestor::dt/following-sibling::dd//span").text
        volume_24h = driver.find_element(By.XPATH, "//div[contains(text(),'Volume (24h')]/ancestor::dt/following-sibling::dd//span").text
        circulating_supply = driver.find_element(By.XPATH, "//div[contains(text(),'Circulating supply')]/ancestor::dt/following-sibling::dd//span").text
        price_change_24h = driver.find_element(By.CSS_SELECTOR, "p.change-text").text
      try:
          rank = driver.find_element(By.XPATH, "//small[contains(text(),'Rank')]/following-sibling::span").text
      except:
          rank = "N/A"


        # Sentiment (more resilient lookup)
        bullish = next((e.text for e in driver.find_elements(By.XPATH, "//span[contains(text(),'%')]") if 'Bullish' in e.get_attribute("outerHTML")), "N/A")
        bearish = next((e.text for e in driver.find_elements(By.XPATH, "//span[contains(text(),'%')]") if 'Bearish' in e.get_attribute("outerHTML")), "N/A")

        # Timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return {
            "timestamp": timestamp,
            "price": price,
            "market_cap": market_cap,
            "volume_24h": volume_24h,
            "circulating_supply": circulating_supply,
            "price_change_24h": price_change_24h,
            "bullish_sentiment": bullish,
            "bearish_sentiment": bearish
            "rank": rank
        }

    except Exception as e:
        print(f"[ERROR] Scraping failed: {e}")
        return None

# --- CSV Writer (Optimized & Robust) ---
def save_to_csv(data, file_name="bitcoin_hourly_data.csv"):
    """Efficiently save or append data to a CSV file with no corruption risk."""
    try:
        df = pd.read_csv(file_name)
    except FileNotFoundError:
        df = pd.DataFrame(columns=data.keys())

    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)

    # Atomic, robust write (avoids file corruption)
    temp_file = file_name + ".tmp"
    df.to_csv(temp_file, index=False, encoding="utf-8-sig", mode="w")
    import os
    os.replace(temp_file, file_name)

# --- Main Execution ---
if __name__ == "__main__":
    print("⏳ Scraping Bitcoin Data...")
    scraped = scrape_bitcoin_data()

    if scraped:
        save_to_csv(scraped)
        print("✅ Data saved to bitcoin_hourly_data.csv")
    else:
        print("❌ Failed to scrape data.")

    driver.quit()
