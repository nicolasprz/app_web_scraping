import os

import requests
from bs4 import BeautifulSoup


def soup_object_to_txt_file(soup: BeautifulSoup, out_path: str):
    """
    Writes a soup indented object to txt file
    """
    with open(out_path, 'w') as f:
        f.write(soup.prettify())


def create_soup_object(url: str, out_path: str) -> BeautifulSoup:
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
        soup_object_to_txt_file(soup, out_path)
        return soup


def scrape_data(soup: BeautifulSoup, tags_out_path: str):
    """
    Scrape data given tags object.
    :param tags: BeautifulSoup object to scrape
    """
    # Get all items from search
    target_li_tags = soup.find_all(
        'li', class_='s-item s-item__pl-on-bottom')[1:]
    for li_tag in target_li_tags:
        soup_object_to_txt_file(li_tag, tags_out_path)
    # Get all items titles
    titles = [li_tag.find('span', role='heading').text
              for li_tag in target_li_tags]
    print(titles)


if __name__ == "__main__":
    URL: str = ('https://www.ebay.fr/sch/i.html?_from='
                'R40&_trksid=p4432023.m570.l1313&_nkw='
                'macbook+air&_sacat=0')
    output_dir: str = f"{os.path.dirname(__file__)}/output/"
    os.makedirs(output_dir, exist_ok=True)
    soup = create_soup_object(URL, f"{output_dir}html.txt")
    scrape_data(soup, f"{output_dir}li_tags.txt")
