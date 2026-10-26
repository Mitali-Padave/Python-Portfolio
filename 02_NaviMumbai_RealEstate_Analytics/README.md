# 🏙️ Navi Mumbai & Greater Panvel Region Real Estate Analytics

An end-to-end data project that scrapes live property listings from MagicBricks, cleans them with Python, stores them in MySQL, and turns them into interactive Power BI dashboards. The goal was to figure out where the real value is in the Navi Mumbai property market.

## What this project does

I wanted to answer a simple question that any homebuyer or investor has: which localities give you the most for your money? To do that, I built a full pipeline from raw web data to business dashboards.

The pipeline has four stages:

1. Scraping - Python (Selenium + BeautifulSoup) to pull around 1,600 live listings from MagicBricks. I started with requests + BeautifulSoup, but the site began blocking automated requests, so I switched to Selenium, which drives a real browser. I checked the site's robots.txt first to make sure the pages I scraped were allowed.
2. Cleaning - pandas and numpy to turn messy text into usable data. This included parsing prices from Crore and Lakh format into numbers, pulling BHK and locality out of listing titles, standardizing area and locality names, handling missing values, and flagging outliers with the IQR method.
3. Storage - MySQL with a relational schema. A localities table linked to a properties table, so the data is properly structured and queryable.
4. Visualization - Power BI. Two main dashboards plus an intro page, a key insights page, and a deep dive page with AI visuals.

## Tools used

Python, pandas, numpy, Selenium, BeautifulSoup, MySQL, Power BI, DAX

## Key insights

- 1,608 listings analyzed; average price ~₹0.99 Cr, ~₹13,218 per sqft, average size ~703 sqft
- 87% of listings are resale, only 13% new construction — a resale-driven market
- 1 and 2 BHK make up 86% of supply — caters to first-time buyers
- Panvel and Kharghar have the most listings
- 3.7x price-per-sqft gap: Seawoods (~₹31,400) vs Taloja (~₹8,400)
- 89% of listings are posted directly by owners

## Key takeaway

Panvel and Taloja offer the best value. A 2BHK there costs roughly a third of what the same space costs in premium areas like Seawoods. If you want space on a budget, the Panvel belt gives you the most sqft per rupee.

## Project structure
NaviMumbai_RealEstate_Analytics/

├── 01_Scraping/

│ ├── MagicBricks_Scraping.ipynb

│ └── MagicBricks_NaviMumbai_raw.xlsx

├── 02_Cleaning/

│ ├── MagicBricks_Data_Cleaning.ipynb

│ └── MagicBricks_NaviMumbai_clean.xlsx

├── 03_SQL/

│ ├── 01_schema.sql

│ └── 02_analysis.sql

└── 04_Dashboard/

├── 01_Introduction.png

├── 02_Market_Overview.png

├── 03_Locality_Explorer.png

├── 04_Key_Influencers.png

├── 05_Decomposition.png

├── 06_Key_Insights.png

└── Real_Estate_MagicBricks.pbix

## Dashboards

The Power BI file has six pages: an introduction, a market overview dashboard, a locality price explorer with a map, a key influencers page, a decomposition tree, and a key insights page.

Screenshots are in the 04_Dashboard folder.

## Live Dashboard

🔗 [View the interactive Power BI dashboard](https://app.powerbi.com/links/6HMgOmTpD5?ctid=21cded39-1d9a-4cb0-8abd-89d2a283d427&pbi_source=linkShare)

## Note

The database password in the cleaning notebook has been replaced with a placeholder. Replace YOUR_PASSWORD with your own MySQL password to run it.

## Author

Mitali Padave  
[GitHub](https://github.com/Mitali-Padave) | [LinkedIn](https://www.linkedin.com/in/mitali-padave-581a2a242/)
