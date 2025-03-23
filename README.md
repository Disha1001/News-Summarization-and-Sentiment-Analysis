# News Summarization & Sentiment Analysis

## Overview
**News Summarization & Sentiment Analysis** is a tool that fetches the latest news articles about a company, summarizes them, performs sentiment analysis, and provides a comparative analysis. Additionally, it generates a **Hindi text-to-speech (TTS) audio summary** of the final sentiment analysis.

## Features
- Fetches **real-time news articles** for any company.
- Summarizes each article in a **single sentence**.
- Performs **sentiment analysis** (Positive, Negative, or Neutral).
- Extracts **key topics** from articles.
- Compares articles to highlight **differences in coverage and sentiment**.
- Provides a **final sentiment analysis** summarizing the overall news sentiment.
- Generates a **Hindi audio summary** of the sentiment analysis.

## Technologies Used
- **Python** → Backend processing
- **FastAPI** → API development
- **Streamlit** → Frontend interface
- **BeautifulSoup** → Web scraping for news articles
- **Groq API** → Summarization, sentiment analysis, and topic extraction
- **Google Translator** → English-to-Hindi translation
- **gTTS** → Hindi text-to-speech audio generation

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Disha1001/News-Summarization-and-Sentiment-Analysis.git
cd News-Summarization-and-Sentiment-Analysis
```
### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
### 3. Run the FastAPI Backend
```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```
### 4. Run the Streamlit Frontend
```bash
streamlit run app.py
```

