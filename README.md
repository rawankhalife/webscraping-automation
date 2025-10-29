# 🪙 Bitcoin Data Scraper & Dashboard

This project automatically scrapes **Bitcoin market data** from [CoinMarketCap](https://coinmarketcap.com/currencies/bitcoin/) and updates a public CSV file and web dashboard using **GitHub Actions**.

---

## 📦 Features
- Automated **Bitcoin data scraping** with Selenium  
- **10-minute interval updates** via GitHub Actions  
- Data saved in `bitcoin_hourly_data.csv`  
- Real-time web dashboard (`index.html` / `bitcoin_v2.html`)  
- Extracted metrics:
  - Current Price  
  - Market Cap  
  - 24-Hour Volume  
  - Circulating Supply  
  - 24-Hour Price Change  
  - Bullish / Bearish Sentiment  
  - Rank  

---

## ⚙️ How It Works
1. `bitcoin_scraper.py` scrapes live data from CoinMarketCap using Selenium (headless Chrome).  
2. The scraped data is appended to `bitcoin_hourly_data.csv`.  
3. A GitHub Action (`.github/workflows/scraper_v2.yml`) runs automatically every 10 minutes.  
4. The latest CSV is committed and used by the dashboard.  
5. `script.js` / `script_v2.js` dynamically fetch the CSV and display the data in the HTML page.

---
pip install -r requirements.txt
python bitcoin_scraper.py
