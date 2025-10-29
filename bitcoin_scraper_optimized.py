from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
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


def safe_get_text(driver, xpath, timeout=15):
    try:
        elem = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.XPATH, xpath))
        )
        txt = elem.text.strip()
        if not txt:
            # fallback in case .text is empty on dynamic sites
            txt = elem.get_attribute("textContent") or ""
            txt = txt.strip()
        return txt if txt else "N/A"
    except (StaleElementReferenceException, TimeoutException):
        # one quick retry for staleness
        try:
            elem = WebDriverWait(driver, timeout).until(
                EC.visibility_of_element_located((By.XPATH, xpath))
            )
            return (elem.text or elem.get_attribute("textContent") or "").strip() or "N/A"
        except Exception:
            return "N/A"
    except Exception:
        return "N/A"


def scrape_bitcoin_data():
    driver.get(URL)
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, '//span[@data-test="text-cdp-price-display"]'))
    )

    def get_sentiment(driver, main_class, sub_class):
        try:
            xpath = f"//span[contains(@class,'{main_class}') and contains(@class,'{sub_class}') and contains(@class,'ratio')]"
            elem = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpath)))
            return elem.text.strip() or elem.get_attribute("textContent").strip() or "N/A"
        except:
            return "N/A"

    data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "price": safe_get_text(driver, '//span[@data-test="text-cdp-price-display"]'),
        "market_cap": safe_get_text(driver, "//dt[contains(., 'Market cap')]/following::dd[1]//span[1]"),
        "volume_24h": safe_get_text(driver, "//dt[.//div[contains(text(),'Volume (24h')]]/following-sibling::dd//span"),
        "circulating_supply": safe_get_text(driver, "//dt[.//div[contains(text(),'Circulating supply')]]/following-sibling::dd//span"),
        "price_change_24h": safe_get_text(driver, "//p[contains(@class, 'change-text')]"),
        "bullish_sentiment": get_sentiment(driver, "sc-65e7f566-0", "cOjBdO"),
        "bearish_sentiment": get_sentiment(driver, "sc-65e7f566-0", "iKkbth")
    }
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
