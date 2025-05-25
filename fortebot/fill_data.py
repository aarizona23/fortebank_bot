from .scraping import main as scrape_data
from .preprocessing import main as preprocess_data
from .tokenization import main as tokenize_data

if __name__ == "__main__":
    """
    Main function to run the data processing pipeline.
    It scrapes data from the Forte Bank website, preprocesses it,
    and tokenizes the text for further use in the chatbot.
    """
    scrape_data()
    preprocess_data()
    tokenize_data()