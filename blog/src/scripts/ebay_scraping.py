"""
Given the page associated to user input, scrapes data on main page.
"""
import os
import re
from typing import Any

import pandas as pd
import requests
from bs4 import BeautifulSoup, Tag
from .items_classes import NbItems
from .scraper import RequestsConnectionError, Scraper

OUTPUT_DIR: str = f"{os.path.dirname(__file__)}/../../output/"


class EBayScraper(Scraper):
    """Class containing scraping methods for BeautifulSoup."""

    def __init__(self, url: str, user_input: str) -> None:
        """Constructor of Scraper class."""
        complete_url = self.get_complete_url(base_url=url, user_input=user_input)
        self.base_soup: BeautifulSoup = self.get_html_soup(complete_url)

    @staticmethod
    def get_html_soup(url: str) -> BeautifulSoup:
        """
        From given url, creates a soup object with HTML source code.
        :param url: url from site to scrap as a string
        :return: global soup object with all html source code
        """
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            if soup.title is not None:
                print(f"Title of page: {soup.title.text.strip(' | eBay')}")
            return soup
        raise RequestsConnectionError(website_name="eBay",
                                      status_code=response.status_code,
                                      error_message=response.text)

    @staticmethod
    def get_complete_url(base_url: str, user_input: str) -> str:
        """
        Given the base URL of the website, returns the complete url with user input.
        :param base_url: base url of eBay website for user research
        :param user_input: user input given from website's form.
        :return: complete url
        """
        return f"{base_url}{user_input.replace(' ', '+')}&_sacat=0"

    @staticmethod
    def get_price(tag: Tag) -> float | list[float]:
        """
        From element tag, gets the price of sold object.
        :param tag: Tag object where price is found
        :return: price as float or list of floats
        """
        list_price = tag.find('span', class_='s-item__price').text.split()
        return float(list_price[-1].replace(',', '').replace('$', ''))

    def get_seller_info(self, soup: BeautifulSoup) -> tuple[float | None, float | None]:
        """
        Given soup object of a certain item from eBay, gets the seller info,
        i.e. its positive feedback percentage and its number of items sold.
        :param soup: soup object containing a single item data
        :return: tuple of two floats with percentage a number of items sold
            (first, positive_feedback_percentage, then nb_items_sold)
        """
        items_list = soup.find_all(
            'div',
            class_='d-stores-info-categories__container__info__section__item'
        )
        positive_feedback_percentage = None
        nb_items_sold = None
        for info in items_list:
            info_str = info.find('span', class_='ux-textspans ux-textspans--BOLD').text
            if '%' in info_str:
                positive_feedback_percentage = self.get_percentage_as_float(info_str)
            else:
                nb_items_sold = self.get_nb_items_sold(info_str)
        return positive_feedback_percentage, nb_items_sold

    @staticmethod
    def get_percentage_as_float(value: str) -> float:
        """
        Given a percentage value as a string, returns it as a float.
        :param value: percentage value, as a string
        :return: floating repr of percentage value, stripped of non digit characters
        """
        return float(value.strip('%'))

    @staticmethod
    def get_nb_items_sold(value: str) -> NbItems:
        """
        Given a number of format '[0-9][K|M]?', returns its value as an integer.
        :param value: value as a string
        :return: same value converted to a NbItems object
        """
        return NbItems.from_str(value)

    @staticmethod
    def get_rating_average(soup: BeautifulSoup) -> float:
        """
        Given soup object of given item, returns the average score of the seller.
        :param soup: soup object of an item on eBay
        :return: average rating score of the seller
        """
        ratings_list = soup.find_all('div', class_='fdbk-detail-seller-rating')
        if not ratings_list:
            return float('nan')
        # Checks if the string containing the number is actually a float
        # between 0 and 5
        floating_pattern = re.compile(r'^(0|[1-4](\.\d+)?|5(\.0*)?)$')
        ratings = []
        for rating in ratings_list:
            rate_str = rating \
                .find('span', class_='fdbk-detail-seller-rating__value').text
            if re.match(floating_pattern, rate_str):
                ratings.append(float(rate_str))
        if ratings:
            return round(sum(ratings) / len(ratings), 3)

    def scrape_item_data(self, soup: BeautifulSoup) -> tuple[float | int | None, ...]:
        """
        Scrapes single item ratings data (from other users of eBay).
        :param soup: soup object containing a single item data
        """
        rating_avg = self.get_rating_average(soup)
        positive_feedback_percentage, nb_items_sold = self.get_seller_info(soup)
        return rating_avg, positive_feedback_percentage, nb_items_sold

    def extract_item_data(self, li_tag: Tag) -> dict[str, Any]:
        """
        Fora given li tag, scrapes its data (i.e. scrapes a single item data).
        :param li_tag: li tag of given article on eBay
        :return: dictionary with a key value pair for each scraped chunk of data
        """
        title = li_tag.find('span', role='heading').text
        price = self.get_price(li_tag)
        item_link = li_tag.find('a', class_='s-item__link').get('href')
        item_soup = self.get_html_soup(url=item_link)
        rating_avg, positive_feedback_percentage, nb_items_sold = self.scrape_item_data(item_soup)
        return {
            'title': title,
            'price_dollars': price,
            'rating_avg': rating_avg,
            'positive_feedback_percentage': positive_feedback_percentage,
            'nb_items_sold': nb_items_sold,
            'item_url': item_link
        }

    def scrape_pages(self) -> pd.DataFrame:
        """
        Scrape data given tags object.
        :return: DataFrame with all scraped data
        """
        # Get all items from search
        target_li_tags = self.base_soup.find_all('li', class_='s-item s-item__pl-on-bottom')[1:]
        data = [self.extract_item_data(li_tag) for li_tag in target_li_tags]
        return pd.DataFrame(data)

    def scrape(self, user_input: str) -> pd.DataFrame:
        """
        Main function. This function is run by this script. Saves scraped data to a pickle file.
        """
        data = self.scrape_pages()
        data.to_pickle(f"{OUTPUT_DIR}scraped_data.pkl")
        return data
