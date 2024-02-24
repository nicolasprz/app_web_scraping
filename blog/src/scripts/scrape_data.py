"""
Given the page associated to user input, scrapes data on main page.
"""
import os
import re
from typing import Optional

import pandas as pd
import requests
from bs4 import BeautifulSoup, Tag

# Test

BASE_URL: str = ('https://www.ebay.com/sch/i.html?_from='
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


def url_to_soup_object(url: str,
                       out_path: Optional[str] = None) -> BeautifulSoup:
    """
    From given url, creates a soup object with HTML source code.
    :param url: url from site to scrap as a string
    :param out_path: path of out text file
    :return: global soup object with all html source code
    """
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        print(f"Title of page: {soup.title.text.strip(' | eBay')}")
        if out_path is not None:
            soup_object_to_txt_file(soup, out_path)
        return soup


def get_complete_url(base_url: str, user_input: str) -> str:
    """
    Given the base URL of the website, returns the complete url with
    user input.
    :param base_url: base url of website
    :param user_input: user input given from website's form.
    :return: complete url
    """
    return f"{base_url}{user_input.replace(' ', '+')}&_sacat=0"


def get_price(tag: Tag) -> float | list[float]:
    """
    From element tag, gets the price of sold object.
    :param tag: Tag object where price is found
    :return: price as float or list of floats
    """
    list_price = tag.find('span', class_='s-item__price').text.split()
    if len(list_price) > 2:
        return [float(element.replace(',', '.').replace('$', ''))
                for element in list_price
                if re.search(r'\d', element)]  # Checks if contains a number
    return float(list_price[0].replace(',', '.').replace('$', ''))


def get_seller_info(soup: BeautifulSoup) -> tuple[float, float]:
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
        info_str = info \
            .find('span', class_='ux-textspans ux-textspans--BOLD').text
        if '%' in info_str:
            positive_feedback_percentage = get_percentage_as_float(info_str)
        else:
            nb_items_sold = get_nb_items_sold(info_str)
    return positive_feedback_percentage, nb_items_sold


def get_percentage_as_float(value: str) -> float:
    """
    Given a percentage value as a string, returns it as a float.
    :param value: percentage value, as a string
    :return: floating repr of percentage value, striped of non digit characters
    """
    return float(value.strip('%'))


def get_nb_items_sold(value: str) -> int:
    """
    # TODO: Add a script to handle millions (maybe an Enum ?).
    Given a number of format '[0-9]K?', returns its value as a integer.
    :param value: value as a string
    :return: same value converted to an integer
    """
    if 'K' in value:
        value = float(value.strip('K')) * 1000
    return int(value)


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
        return sum(ratings) / len(ratings)


def scrape_item_data(soup: BeautifulSoup) -> tuple[float | int, ...]:
    """
    Scrapes single item ratings data (from other users of eBay).
    :param soup: soup object containing a single item data
    """
    rating_avg = get_rating_average(soup)
    positive_feedback_percentage, nb_items_sold = get_seller_info(soup)
    print(f"{rating_avg=}")
    print(f"{positive_feedback_percentage=}")
    print(f"{nb_items_sold=}\n")
    return rating_avg, positive_feedback_percentage, nb_items_sold


def scrape_pages(soup: BeautifulSoup, tags_out_path: str) -> pd.DataFrame:
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
    ratings = []
    percentages = []
    nb_items = []
    for li_tag in target_li_tags:
        soup_object_to_txt_file(li_tag, tags_out_path, write_type='a')
        titles.append(li_tag.find('span', role='heading').text)
        price = get_price(li_tag)
        prices.append(price)
        single_item = li_tag.find('a', class_='s-item__link')
        single_item_link = single_item.get('href')
        item_soup = url_to_soup_object(url=single_item_link)
        (
            rating_avg, positive_feedback_percentage, nb_items_sold
        ) = scrape_item_data(item_soup)
        ratings.append(rating_avg)
        percentages.append(positive_feedback_percentage)
        nb_items.append(nb_items_sold)
    return pd.DataFrame(dict(
        title=titles, price_dollars=prices, rating_avg=ratings,
        positive_feedback_percentage=percentages,
        nb_items_sold=nb_items
    ))


def main(user_input: str) -> pd.DataFrame:
    """
    Main function. This function is run by this script. Saves scraped data
    to a csv file.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    URL = get_complete_url(BASE_URL, user_input)
    soup = url_to_soup_object(URL, f"{OUTPUT_DIR}html.txt")
    data = scrape_pages(soup, f"{OUTPUT_DIR}li_tags.txt")
    data.to_csv(f"{OUTPUT_DIR}scraped_data.csv", index=False, sep=';')
    return data


if __name__ == "__main__":
    # To test script locally
    main("clavier logitech")
