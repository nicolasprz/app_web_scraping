import pandas as pd
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from .scraper import Scraper, RequestsConnectionError


def get_complete_url(base_url: str, user_input: str) -> str:
    """
    Given the base URL of the website, returns the complete url with user input.
    :param base_url: base url of eBay website for user research
    :param user_input: user input given from website's form.
    :return: complete url
    """
    return f"{base_url}{user_input.replace(' ', '+')}"


class AmazonScraper(Scraper):
    """Processing class for Amazon website scraping"""

    def __init__(self, url: str, user_input: str):
        complete_url = get_complete_url(base_url=url, user_input=user_input)
        self.base_soup: BeautifulSoup = self.get_html_soup(url=complete_url)

    @staticmethod
    def get_html_soup(url: str) -> BeautifulSoup:
        """
        From given url, creates a soup object with HTML source code.
        :param url: url from site to scrap as a string
        :return: global soup object with all html source code
        """
        user_agent = UserAgent()
        response = requests.get(url, headers={'User-Agent': user_agent.random})
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            if soup.title is not None:
                print(f"Title of page: {soup.title.text}")
            return soup
        raise RequestsConnectionError(website_name="Amazon", status_code=response.status_code,
                                      error_message=response.text)

    def scrape(self, user_input: str) -> pd.DataFrame:
        """Main function. Saves scraped data to a pickle file."""
        return pd.DataFrame()
