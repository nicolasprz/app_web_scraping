"""
Script defining classes and Protocol needed to scrape a website with BeautifulSoup
"""
from typing import Protocol
from bs4 import BeautifulSoup
import pandas as pd


class RequestsConnectionError(Exception):
    """Raised when connection could not be made to the website."""

    def __init__(self, website_name: str, status_code: int, error_message: str) -> None:
        super().__init__(
            f'Connection could not be made to website "{website_name}" (error {status_code})\n{error_message}'
        )


class Scraper(Protocol):
    """Protocol class for Scraper classes."""

    @staticmethod
    def get_html_soup(url: str) -> BeautifulSoup:
        """Given the url to a website, requests html code and returns it as a BeautifulSoup object."""

    def scrape(self, user_input: str) -> pd.DataFrame:
        """Method used to scrape all data needed on wanted website, and returns the result as a pandas DataFrame."""
