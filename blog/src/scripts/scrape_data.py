"""
Given the page associated to user input, scrapes data on main page.
"""
# !/usr/bin/env python3.8
import os
import re

import pandas as pd
import requests
from bs4 import BeautifulSoup, Tag

BASE_URL: str = ('https://www.ebay.fr/sch/i.html?_from='
                 'R40&_trksid=p4432023.m570.l1313&_nkw=')
OUTPUT_DIR: str = f"{os.path.dirname(__file__)}/../../output/"


def soup_object_to_txt_file(soup: BeautifulSoup, out_path: str,
                            write_type: str = 'w') -> None:
    """
    Writes a soup indented object to txt file
    :param soup: soup object to write
    :param out_path: path of output text file
    :param write_type: single character ('w', 'a') telling whether to erase
        content and write object, or append at the end of the file.
    """

    with open(out_path, write_type) as f:
        f.write(soup.prettify())


def url_to_soup_object(url: str, out_path: str) -> BeautifulSoup:
    """
    From given url, creates a soup object with HTML source code.
    :param url: url from site to scrap as a string
    :param out_path: path of out text file
    :return: global soup object with all html source code
    """
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        print(f"Title of page: {soup.title.text}")
        if out_path is not None:
            soup_object_to_txt_file(soup, out_path)
        return soup


def get_price(tag: Tag) -> float | list[float]:
    """
    From element tag, gets the price of sold object.
    :param tag: Tag object where price is found
    :return: price as float or list of floats
    """
    list_price = tag.find('span', class_='s-item__price').text.split()
    if len(list_price) > 2:
        return [float(element.replace(',', '.'))
                for element in list_price
                if re.search(r'\d', element)]  # Checks if contains a number
    return float(list_price[0].replace(',', '.'))


def scrape_main_page(soup: BeautifulSoup, tags_out_path: str) -> pd.DataFrame:
    """
    Scrape data given tags object.
    :param soup: BeautifulSoup object to scrape
    :param tags_out_path: path of output text code
    """
    # Get all items from search
    target_li_tags = soup.find_all(
        'li', class_='s-item s-item__pl-on-bottom')[1:]
    with open(tags_out_path, 'w'):
        pass
    titles = []
    prices = []
    for li_tag in target_li_tags:
        soup_object_to_txt_file(li_tag, tags_out_path, write_type='a')
        titles.append(li_tag.find('span', role='heading').text)
        price = get_price(li_tag)
        prices.append(price)
    return pd.DataFrame(dict(titles=titles, prices=prices))


def get_complete_url(base_url: str, user_input: str) -> str:
    """
    Given the base URL of the website, returns the complete url with
    user input.
    :param base_url: base url of website
    :param user_input: user input given from website's form.
    :return: complete url
    """
    return f"{base_url}{user_input.replace(' ', '+')}&_sacat=0"


def main(user_input: str) -> None:
    """
    Main function. This function is run by this script. Saves scraped data
    to a csv file.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    URL = get_complete_url(BASE_URL, user_input)
    soup = url_to_soup_object(URL, f"{OUTPUT_DIR}html.txt")
    data = scrape_main_page(soup, f"{OUTPUT_DIR}li_tags.txt")
    data.to_csv(f"{OUTPUT_DIR}scraped_data.csv", index=False, sep=';')
