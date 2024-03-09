import pandas as pd

SORTING_ORDER = ["nb_items_int", "positive_feedback_percentage", "rating_avg", "price_dollars"]


def sort_scraped_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Given the DataFrame with scraped data, sorts it along SORTING_ORDER variable
    :param df: DataFrame with scraped data
    :return: sorted DataFrame
    """
    df['nb_items_int'] = df['nb_items_sold'].map(lambda nb: nb.as_int)
    assert all(col in df.columns for col in SORTING_ORDER)
    return df.sort_values(by=SORTING_ORDER, ascending=(False, False, False, True), ignore_index=True)


def remove_items_not_full_input(df: pd.DataFrame, user_input: str) -> pd.DataFrame:
    """
    Removes items that do not have the full user input in their title
    :param df: DataFrame to filter
    :param user_input: given user input fetched from website form
    :return: filtered DataFrame
    """
    return df.loc[df.title.str.contains(user_input, case=False)].reset_index(drop=True)


def main(scraped_data: pd.DataFrame, user_input: str) -> pd.DataFrame:
    """
    Processes scraped data from eBay and returns a copy of it after processing.
    :param scraped_data: data that was scraped on eBay website
    :param user_input: input of user on web scraping website
    :return: sorted DataFrame to display on website
    """
    resulting_df = sort_scraped_df(scraped_data)
    resulting_df = remove_items_not_full_input(resulting_df, user_input)
    return resulting_df
