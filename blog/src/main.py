"""
Main script. This script is called by python anywhere website to scrape data on given URL.
"""
import pandas as pd

from .scripts import ebay_scraping, compute_item_data

EBAY_BASE_URL: str = 'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p4432023.m570.l1313&_nkw='


def scrape_ebay(user_input: str) -> pd.DataFrame:
    """Runs scraping scripts for eBay scraping."""
    scraper = ebay_scraping.EBayScraper(url=EBAY_BASE_URL, user_input=user_input)
    scraped_data = scraper.scrape(user_input)
    scraped_data = compute_item_data.main(scraped_data, user_input)
    scraped_data.index = scraped_data.index.values + 1
    scraped_data = scraped_data.reset_index()
    return scraped_data.head(10)


def main(user_input: str, website: str) -> pd.DataFrame | None:
    """Runs processing scripts given the user input string, and the choice of website to scrape."""
    if website.lower() == 'ebay':
        return scrape_ebay(user_input)
    elif website.lower() == 'amazon':
        pass
