"""
Main script. This script is called by python anywhere website to scrape data
on given URL.
"""
from .scripts import scrape_data


def main(input: str) -> str:
    """Runs processing scripts given the user input string."""
    scrape_data.main(user_input=input)
    return "OK"
