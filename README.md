# webscraping-automation
This project automatically scrapes Bitcoin market data from CoinMarketCap
 and updates a public CSV file and web dashboard using GitHub Actions.

📦 Features

Automated Bitcoin data scraping with Selenium

10-minute interval updates via GitHub Actions

Data saved in bitcoin_hourly_data.csv

Real-time web dashboard (index.html / bitcoin_v2.html)

Extracted metrics:

Current Price

Market Cap

24-Hour Volume

Circulating Supply

24-Hour Price Change

Bullish / Bearish Sentiment

Rank

⚙️ How It Works

bitcoin_scraper.py scrapes live data from CoinMarketCap using Selenium (headless Chrome).

The scraped data is appended to bitcoin_hourly_data.csv.

A GitHub Action (.github/workflows/scraper_v2.yml) runs automatically every 10 minutes.

The latest CSV is committed and used by the dashboard.

script.js / script_v2.js dynamically fetch the CSV and display the data in the HTML page.

🧰 Tech Stack

Python 3

Selenium + Pandas

ChromeDriver (via webdriver_manager)

HTML / CSS / JavaScript

GitHub Actions

🚀 Manual Run
pip install -r requirements.txt
python bitcoin_scraper.py


or run the optimized version:

python bitcoin_scraper_optimized.py


The script generates / updates:

bitcoin_hourly_data.csv

🖥️ Dashboard

index.html → Displays the data table

bitcoin_v2.html → Enhanced dashboard version

script.js / script_v2.js → Fetch CSV and populate the dashboard

style.css → Styling for layout and visuals

📂 Repository Structure
.github/workflows/      → GitHub Actions automation
bitcoin_scraper.py      → Main scraper script
bitcoin_scraper_optimized.py → Optimized scraper
bitcoin_hourly_data.csv → Auto-updated dataset
index.html / bitcoin_v2.html → Dashboard files
script.js / script_v2.js → Data fetching scripts
style.css               → Dashboard styling
README.md               → Project overview

🧠 Notes

The scraper adapts to CoinMarketCap’s changing HTML structure using flexible XPaths.
