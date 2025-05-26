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

## Web Scraping ForteBank Services 
This project includes a custom web scraper that collects information about banking services offered by ForteBank, including cards, credits, deposits, transfers, and salary projects.

### 🛠 Technologies Used 
- Selenium – for browser automation and interacting with dynamic content
- BeautifulSoup – for parsing HTML content
- webdriver_manager – for automatic ChromeDriver management
- csv – for saving data in structured format

### 📋 Collected Services 
The scraper collects data about the following services:
- Bank Cards
- Credits (Loans)
- Deposits
- Money Transfers
- Salary Projects

### 📄 Data Fields 
Each scraped service includes:
- service_name – the category of the service (e.g., "card", "credit")
- name – the title of the individual product
- description – a short summary or explanation
- url – a link to the service details (if available)

### 📂 Output File 
The collected data is saved into a single CSV file:

```bash
data/raw/services.csv
```

## 🧹 Preprocessing and 🧠 Tokenization Pipeline

To prepare the scraped data for semantic search or machine learning tasks, this project includes a **preprocessing and tokenization pipeline** consisting of two main stages.

---

## 🧹 1. Preprocessing (`preprocess.py`) 

This stage cleans and prepares the raw service descriptions.

#### Key Steps

| Function             | Purpose                                                                 |
|----------------------|-------------------------------------------------------------------------|
| `delete_null_rows()` | Removes rows with missing or `"null"` values in `name` or `description` |
| `clean_text()`       | Cleans unwanted characters (quotes, bullets, line breaks, etc.)         |
| `combine_rows()`     | Merges `service_name`, `name`, and `description` into a `full_text`     |

Output
Cleaned data is saved to:

```bash
data/processed/services_cleaned.csv
```

## 🧠 2. Tokenization (tokenize.py)
This stage converts each cleaned text entry into a dense vector embedding using a multilingual SentenceTransformer model.

- tokenize_text(): Encodes each full_text using the cointegrated/LaBSE-en-ru model
- The model supports both English and Russian, ideal for bilingual banking data.

Embeddings are stored as lists of floats in a new column called embedding.

Model Used
```python
SentenceTransformer("cointegrated/LaBSE-en-ru")
```
Output
Tokenized and embedded data is saved to:

```bash
data/processed/services_with_embeddings.csv
```

## 🔍 ServiceSearch Model Overview

The `ServiceSearch` class performs semantic search over banking services using the multilingual model `cointegrated/LaBSE-en-ru`.

---

### 🧠 How It Works

1. **Initialization (`__init__`)**  
   Loads the query, SentenceTransformer model, and preprocessed services with embeddings.

2. **Category Detection (`detect_category`)**  
   Filters services based on category-related keywords in the query (e.g., "кредит", "депозит").

3. **Text Similarity Search (`get_results`)**  
   Encodes the query and compares it to service embeddings using cosine similarity to find the most relevant services.

4. **Response Formatting (`search`)**  
   Returns the top result in a friendly text format with a URL. If no matches are found, returns a fallback message.

---

### ✅ Example

```python
search = ServiceSearch("хочу вклад в долларах")
print(search.search())
```

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

URL for the Demonstration video:
https://drive.google.com/file/d/1y1bWdMWM92jMI4DZM5-AQFf9Q1OaWIV9/view?usp=sharing

<img width="1128" alt="image" src="https://github.com/user-attachments/assets/365a9488-7ee1-4337-8367-c5d61acbed7c" />

Here are some example questions you can ask:

💳 Карты
- Какие карты есть в ForteBank?
- В чём разница между картами Blue и Black?
- Какие карты дают кешбэк?
- Есть ли карта для путешествий?
- Какие карты можно оформить бесплатно?

💰 Кредиты
- Какие есть условия для экспресс-кредита?
- Что такое залоговый кредит?
- Как работает рефинансирование?
- Можно ли получить автокредит без первоначального взноса?
- Какие кредиты доступны на сумму до 10 млн тенге?

### 🏦 Депозиты
- Какие депозиты доступны в тенге и долларах?
- Есть ли депозиты со снятием?
- Какой минимальный вклад для сберегательного депозита?

### 🔁 Переводы
- Как перевести деньги по номеру телефона?
- Сколько стоит перевод на карту?
- Можно ли перевести деньги за границу?
- Что такое перевод через Золотую Корону?
- В чём разница между Alem и Swift переводами?

### 🧾 Зарплатный проект
- Какую карту лучше выбрать для зарплаты?
- Какие условия по карте Blue в рамках зарплатного проекта?
- Что входит в зарплатную карту Solo?
- Есть ли бонусы за использование зарплатной карты?



