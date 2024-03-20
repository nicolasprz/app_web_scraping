import os
from typing import Any
import pandas as pd
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup, Tag
from .scraper import Scraper, RequestsConnectionError

OUTPUT_DIR: str = f"{os.path.dirname(__file__)}/../../output/"


class AmazonScraper(Scraper):
    """Processing class for Amazon website scraping."""

    def __init__(self, url: str, user_input: str):
        complete_url = self.get_complete_url(base_url=url, user_input=user_input)
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

    @staticmethod
    def get_complete_url(base_url: str, user_input: str) -> str:
        """
        Given the base URL of the website, returns the complete url with user input.
        :param base_url: base url of eBay website for user research
        :param user_input: user input given from website's form.
        :return: complete url
        """
        return f"{base_url}{user_input.replace(' ', '+')}"

    @staticmethod
    def get_price(tag: Tag) -> float | None:
        """
        From element tag, gets the price of sold object.
        :param tag: Tag object where price is found
        :return: price as float or None if no price is found
        """
        whole_part = tag.find('span', {'class': 'a-price-whole'}).text.strip(',')
        decimal_part = tag.find('span', {'class': 'a-price-fraction'}).text
        try:
            return float(f"{whole_part}.{decimal_part}")
        except ValueError:
            print(f"no price: {whole_part}.{decimal_part}")
            return None

    def extract_item_data(self, tag: Tag) -> dict[str, Any]:
        """
        Fora given li tag, scrapes its data (i.e. scrapes a single item data).
        :param tag: li tag of given article on eBay
        :return: dictionary with a key value pair for each scraped chunk of data
        """
        title = tag.find('span', {'class': 'a-size-base-plus a-color-base a-text-normal'}).text
        print(f"Scraped item '{title}'")
        price = self.get_price(tag)
        # item_link = tag.find('a', class_='s-item__link').get('href')
        # item_soup = self.get_html_soup(url=item_link)
        # rating_avg, positive_feedback_percentage, nb_items_sold = self.scrape_item_data(item_soup)
        return {
            'title': title,
            'price_dollars': price,
            # 'rating_avg': rating_avg,
            # 'positive_feedback_percentage': positive_feedback_percentage,
            # 'nb_items_sold': nb_items_sold,
            # 'item_url': item_link
        }

    def scrape_pages(self) -> pd.DataFrame:
        """
        Scrape data given tags object.
        :return: DataFrame with all scraped data
        """
        # Get all items from search (on first page)
        target_tags = self.base_soup.find_all('div', {'data-component-type': 's-search-result'})
        data = [self.extract_item_data(tag) for tag in target_tags]
        return pd.DataFrame(data)

    def scrape(self, user_input: str) -> pd.DataFrame:
        """Main function. Saves scraped data to a pickle file."""
        data = self.scrape_pages()
        data.to_pickle(f"{OUTPUT_DIR}scraped_data.pkl")
        return data
