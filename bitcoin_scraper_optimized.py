from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
import pandas as pd
import os, logging
from datetime import datetime

# --- Setup ---
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

ua = UserAgent()
options.add_argument(f"user-agent={ua.random}")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
URL = "https://coinmarketcap.com/currencies/bitcoin/"

def safe_get_text(driver, xpath):
    try:
        return driver.find_element(By.XPATH, xpath).text
    except:
        return "N/A"

def scrape_bitcoin_data():
    driver.get(URL)
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, '//span[@data-test="text-cdp-price-display"]'))
    )

    data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "price": safe_get_text(driver, '//span[@data-test="text-cdp-price-display"]'),
        "market_cap": safe_get_text(driver, "//dt[.//div[contains(text(),'Market cap')]]/following-sibling::dd//span"),
        "volume_24h": safe_get_text(driver, "//dt[.//div[contains(text(),'Volume (24h')]]/following-sibling::dd//span"),
        "circulating_supply": safe_get_text(driver, "//dt[.//div[contains(text(),'Circulating supply')]]/following-sibling::dd//span"),
        "price_change_24h": safe_get_text(driver, "//p[contains(@class, 'change-text')]")
    }

    try:
        bullish = driver.find_elements(By.XPATH,
            "//span[contains(@class, 'sc-65e7f566-0 cOjBdO') and contains(@class, 'ratio')]")
        bearish = driver.find_elements(By.XPATH,
            "//span[contains(@class, 'sc-65e7f566-0 iKkbth') and contains(@class, 'ratio')]")

        data["bullish_sentiment"] = bullish[0].text if bullish else "N/A"
        data["bearish_sentiment"] = bearish[0].text if bearish else "N/A"
    except:
        data["bullish_sentiment"] = "N/A"
        data["bearish_sentiment"] = "N/A"

    return data

def save_to_csv(data, file_name="bitcoin_hourly_data_v2.csv"):
    df = pd.DataFrame([data])
    df.to_csv(file_name, mode='a', header=not os.path.exists(file_name), index=False)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
    logging.info("Scraping Bitcoin Data...")
    data = scrape_bitcoin_data()
    save_to_csv(data)
    logging.info("Data saved successfully.")
    driver.quit()
