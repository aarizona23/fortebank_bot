# 💬 ForteBank Chatbot

An intelligent chatbot system for ForteBank that uses NLP techniques (Sentence-BERT embeddings) to understand user queries and return relevant banking service information.

## 🚀 Features

- Used Web Scraping technologies (Selenium, BeautifulSoup) to collect data from ForteBank pages about cards, credits, deposits, transfers, salary projects
- Preprocessed and embedded data from ForteBank service descriptions
- Sentence-BERT model to convert user queries into semantic embeddings
- Semantic search using cosine similarity
- Simple web-based interface via FastAPI
- Source links included with each result
- Modular structure for easy maintenance

---

## ⚙️ Installation

1. **Clone the repo:**
```bash
git clone https://github.com/aarizona23/fortebank_bot.git
cd fortebank_bot
```

2. **Create a virtual environment:**

```bash
python -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **🧠 Run the App**
```bash
uvicorn api.main:app --reload
```
Then open your browser at: http://127.0.0.1:8000

