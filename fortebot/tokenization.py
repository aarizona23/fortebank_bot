import pandas as pd
from sentence_transformers import SentenceTransformer

def tokenize_text(frame: pd.DataFrame) -> pd.DataFrame:
    """
    Tokenizes the text in the 'description' column of the DataFrame using a pre-trained SentenceTransformer model.
    :param frame: DataFrame containing a 'description' column with text data
    :return: DataFrame with an additional 'embedding' column containing the embeddings of the descriptions
    """

    model = SentenceTransformer("cointegrated/LaBSE-en-ru")
    frame['embedding'] = frame['full_text'].apply(lambda x: model.encode(x, convert_to_tensor=True).cpu().tolist())
    return frame

def main():
    """
    Main function to read the cleaned services data, tokenize the text using SentenceTransformer,
    :return:
    """
    with open("data/processed/services_cleaned.csv", "r", encoding="utf-8") as file:
        df = pd.read_csv(file)
    df = tokenize_text(df)
    df.to_csv("data/processed/services_with_embeddings.csv", index=False, encoding="utf-8")
