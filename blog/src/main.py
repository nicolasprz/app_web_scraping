"""
Main script. This script is called by python anywhere website to scrape data on given URL.
"""
import pandas as pd

from .scripts import scrape_data, compute_item_data


def main(user_input: str) -> pd.DataFrame:
    """Runs processing scripts given the user input string."""
    scraped_data: pd.DataFrame = scrape_data.main(user_input=user_input)
    # scraped_data = compute_item_data.main(scraped_data)
    scraped_data.index = scraped_data.index.values + 1
    scraped_data = scraped_data.reset_index()
    return scraped_data.head(10)
