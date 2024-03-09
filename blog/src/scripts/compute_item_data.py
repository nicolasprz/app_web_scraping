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


def main(scraped_data: pd.DataFrame) -> pd.DataFrame:
    """Processes scraped data from eBay and returns a copy of it after processing."""
    return sort_scraped_df(df=scraped_data)

