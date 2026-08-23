# 🏙️ Navi Mumbai Real Estate Analytics

An end-to-end data project that scrapes live property listings from MagicBricks, cleans them with Python, stores them in MySQL, and turns them into interactive Power BI dashboards. The goal was to figure out where the real value is in the Navi Mumbai property market.

## What this project does

I wanted to answer a simple question that any homebuyer or investor has: which localities in Navi Mumbai give you the most for your money? To do that, I built a full pipeline from raw web data to business dashboards.

The pipeline has four stages:

1. Scraping - Python (requests + BeautifulSoup) to pull around 750 live listings from MagicBricks. I checked the site's robots.txt first to make sure the pages I scraped were allowed.
2. Cleaning - pandas and numpy to turn messy text into usable data. This included parsing prices from Crore and Lakh format into numbers, pulling BHK and locality out of listing titles, standardizing area, and handling missing values.
3. Storage - MySQL with a relational schema. A localities table linked to a properties table, so the data is properly structured and queryable.
4. Visualization - Power BI. Two main dashboards plus an intro page, a key insights page, and a deep dive page with AI visuals.

## Tools used

Python, pandas, numpy, BeautifulSoup, MySQL, Power BI, DAX

## Key insights

- The market average works out to about 1.34 Cr, roughly 15,000 per sqft, on an average size of about 867 sqft.
- 82 percent of listings are New Property, and only 18 percent are Resale. Navi Mumbai is a growth and construction-driven market.
- 76 percent of listings are 2BHK, which is the dominant demand segment.
- Kharghar and Panvel have the most listings, so they are the busiest markets.
- Seawoods is the most expensive locality at around 32,000 per sqft. Panvel and Taloja are the best value at roughly 8,000 to 10,000 per sqft.
- Owners post the most listings, far more than agents or builders.

## Key takeaway

Panvel and Taloja offer the best value in Navi Mumbai. A 2BHK there costs roughly a third of what the same space costs in premium areas like Seawoods. If you want space on a budget, the Panvel belt gives you the most sqft per rupee.

## Project structure

```
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
```

## Dashboards

The Power BI file has five pages: an introduction, key insights, a market overview dashboard, a locality price explorer with a map, and a deep dive page using Key Influencers and a Decomposition Tree.

Screenshots are in the 04_Dashboard/screenshots folder.

## Note

The database password in the cleaning notebook has been replaced with a placeholder. Replace YOUR_PASSWORD with your own MySQL password to run it.

## Author

Mitali Padave  
[GitHub](https://github.com/Mitali-Padave) | [LinkedIn](https://www.linkedin.com/in/mitali-padave-581a2a242/)
