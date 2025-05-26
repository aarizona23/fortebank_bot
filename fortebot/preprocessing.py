import pandas as pd
import re

def delete_null_rows(df) -> pd.DataFrame:
    """
    Removes rows from the df where the 'name' or 'description' columns are null
    or contain the string "null".
    :param df:
    :return: df
    """
    df = df[df["name"] != "null"]
    df = df[df["description"] != "null"]
    df = df.dropna(subset=["name", "description"])
    return df.reset_index(drop=True)

def clean_text(text) -> str:
    """
    This function removes characters such as bullet points, quotes, and newlines,
    and replaces multiple spaces with a single space.
    :param text:
    :return: text: str
    """
    text = re.sub(r"[\"“”«»\n]", " ", text)
    text = re.sub(r"[•]", ".", text)
    text = re.sub(r"\s+", " ", text).strip()
    text = text.replace("Подробнее", "")
    return text

def combine_rows(df: pd.DataFrame) -> pd.DataFrame:
    """
    Combines the 'service_name', 'name' and 'description' columns into a single 'full_text' column.
    :param df: DataFrame to combine
    :return: Combined DataFrame
    """
    df["full_text"] = df.apply(
        lambda row: f"{row['service_name']}. {row['name']}. {row['description']}", axis=1
    )
    df = df.drop(columns=["name", "description"])
    return df

def main():
    """
    Main function to clean the services data.
    Reads the raw data from a CSV file, cleans it by removing null rows,
    and applying text cleaning functions to the 'description' and 'name' columns.
    Finally, it saves the cleaned data to a new CSV file.
    """

    df = pd.read_csv("data/raw/services.csv")
    df = delete_null_rows(df)
    df["description"] = df["description"].fillna("").apply(clean_text)
    df = combine_rows(df)
    df.to_csv("data/processed/services_cleaned.csv", index=False, encoding="utf-8")
    print("Data cleaned and saved to data/processed/services_cleaned.csv")
