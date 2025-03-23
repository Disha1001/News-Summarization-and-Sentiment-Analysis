News Summarization & Sentiment Analysis
Overview
News Summarization & Sentiment Analysis is a tool that fetches the latest news articles about a company, summarizes them, performs sentiment analysis, and provides a comparative analysis. Additionally, it generates a Hindi text-to-speech (TTS) audio summary of the final sentiment analysis.

Features
Fetches real-time news articles for any company.

Summarizes each article in a single sentence.

Performs sentiment analysis (Positive, Negative, or Neutral).

Extracts key topics from articles.

Compares articles to highlight differences in coverage and sentiment.

Provides a final sentiment analysis summarizing the overall news sentiment.

Generates a Hindi audio summary of the sentiment analysis.

Technologies Used
Python (Backend processing)

FastAPI (API development)

Streamlit (Frontend interface)

BeautifulSoup (Web scraping for news articles)

Groq API (For summarization, sentiment analysis, and topic extraction)

Google Translator (For English-to-Hindi translation)

gTTS (For Hindi text-to-speech audio generation)

Installation
Clone the repository:

bash
Copy
Edit
git clone <repository-url>
cd <repository-folder>
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Run the FastAPI backend:

bash
Copy
Edit
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
Run the Streamlit frontend:

bash
Copy
Edit
streamlit run app.py
Usage
Enter a company name in the input field.

Click "Generate Report" to fetch and analyze news.

Once the report is ready, you can:

Download the full report as a JSON file.

Download the Hindi audio summary.

Deployment
You can deploy this project on:

Hugging Face Spaces (for Streamlit apps)

Render or AWS EC2 (for FastAPI backend)

License
This project is licensed under the MIT License.
