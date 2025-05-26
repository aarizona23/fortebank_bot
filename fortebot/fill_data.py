import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fortebot.scraping import main as scrape_data
from fortebot.preprocessing import main as preprocess_data
from fortebot.tokenization import main as tokenize_data

if __name__ == "__main__":
    """
    Main function to run the data processing pipeline.
    It scrapes data from the Forte Bank website, preprocesses it,
    and tokenizes the text for further use in the chatbot.
    """
    scrape_data()
    preprocess_data()
    tokenize_data()