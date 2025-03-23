import requests
import json
import time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from gtts import gTTS
from deep_translator import GoogleTranslator
import os

# Groq API Configuration
GROQ_API_KEY = "your-groq-api"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# Function to call Groq API with retry handling
def call_groq_api(prompt, max_tokens=100, retries=5, wait_time=2):
    for attempt in range(retries):
        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": max_tokens
        }
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
        
        response = requests.post(GROQ_URL, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"].strip()
        elif response.status_code == 429:
            print(f"Rate Limit Reached! Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
            wait_time *= 2
        else:
            return "Error in API response."
    return "API Error: Maximum Retries Reached"

# Function to extract latest news articles about a company
def extract_news_articles(company_name, num_articles=5):  # Ensure num_articles = 5
    ua = UserAgent()
    headers = {"User-Agent": ua.random}
    search_url = f"https://www.bing.com/news/search?q={company_name}&FORM=HDRSC6"
    
    response = requests.get(search_url, headers=headers, timeout=10)
    if response.status_code != 200:
        return None
    
    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("a", class_="title") or soup.find_all("a")
    
    if not articles:
        return None
    
    article_data = []
    seen_links = set()

    for article in articles:
        if len(article_data) >= num_articles:  
            break

        title = article.get_text(strip=True)
        link = article.get("href")
        
        if not link.startswith("http") or link in seen_links:
            continue  
        
        seen_links.add(link)

        try:
            article_response = requests.get(link, headers=headers, timeout=5)
            article_soup = BeautifulSoup(article_response.text, "html.parser")
            full_text = " ".join(p.get_text() for p in article_soup.find_all("p"))
            if not full_text:
                full_text = title  
        except:
            full_text = title

        article_data.append({"Title": title, "Text": full_text, "Link": link})
    
    return article_data


# Function to summarize a news article
def summarize_text(text):
    prompt = f"Summarize this news article in one sentence:\n\n{text[:1500]}"
    return call_groq_api(prompt, max_tokens=50)

# Function to extract key topics from an article
def extract_topics(text):
    prompt = f"List 3-5 key topics from this article as comma-separated values:\n\n{text[:800]}"
    topics_text = call_groq_api(prompt, max_tokens=50)
    return [topic.strip() for topic in topics_text.split(",") if topic.strip()]

# Function to determine sentiment of an article
def detect_sentiment(text):
    prompt = f"Determine the sentiment of this article as exactly one word: Positive, Negative, or Neutral. Do not explain.\n\n{text[:800]}"
    return call_groq_api(prompt, max_tokens=1).strip()

# Function to translate English text to Hindi
def translate_to_hindi(text):
    try:
        return GoogleTranslator(source="en", target="hi").translate(text)
    except:
        return text

# Function to generate Hindi text-to-speech (TTS) from text
def generate_hindi_tts(text, output_file):
    hindi_text = translate_to_hindi(text)
    try:
        tts = gTTS(hindi_text, lang="hi")
        tts.save(output_file)
        return output_file
    except:
        return None

# Function to perform comparative analysis of extracted articles
def compare_articles(company_name, articles):
    sentiment_distribution = {
        "Positive": sum(1 for a in articles if a["Sentiment"].strip() == "Positive"),
        "Negative": sum(1 for a in articles if a["Sentiment"].strip() == "Negative"),
        "Neutral": sum(1 for a in articles if a["Sentiment"].strip() == "Neutral"),
    }
    
    coverage_differences = []
    for i in range(len(articles)):
        for j in range(i + 1, len(articles)):
            article1, article2 = articles[i], articles[j]
            prompt = f"""
            Compare these two news articles:
            - {article1['Title']} (Summary: {article1['Summary']})
            - {article2['Title']} (Summary: {article2['Summary']})
            Provide a short comparison and impact statement.
            """
            comparison = call_groq_api(prompt, max_tokens=80)
            coverage_differences.append({
                "Comparison": f"{article1['Title']} vs {article2['Title']}",
                "Impact": comparison
            })
            time.sleep(2)
    
    common_topics = set.intersection(*[set(a["Topics"]) for a in articles]) if articles else set()
    
    final_sentiment_prompt = f"""
    Analyze the overall sentiment of the extracted news articles about {company_name}.
    Summarize whether the coverage is mostly positive, negative, or mixed.
    Then, briefly describe its potential impact on {company_name}, such as stock trends, market confidence, or risks.
    
    Articles Sentiments: {[article['Sentiment'] for article in articles]}
    """
    final_sentiment = call_groq_api(final_sentiment_prompt, max_tokens=50)
    
    return {
        "Comparative Sentiment Score": {
            "Sentiment Distribution": sentiment_distribution,
            "Coverage Differences": coverage_differences,
            "Topic Overlap": {"Common Topics": list(common_topics)},
        },
        "Final Sentiment Analysis": final_sentiment
    }

# Function to fetch, analyze, and process news articles
def main(company_name):
    news_articles = extract_news_articles(company_name, num_articles=10)
    if not news_articles:
        return {"error": "No news articles found."}
    
    articles_data = []
    for article in news_articles:
        summary = summarize_text(article["Text"])
        sentiment = detect_sentiment(article["Text"])
        topics = extract_topics(article["Text"])
        articles_data.append({
            "Title": article["Title"],
            "Summary": summary,
            "Sentiment": sentiment,
            "Topics": topics,
            "Link": article["Link"]
        })
    
    analysis_results = compare_articles(company_name, articles_data)
    hindi_tts = generate_hindi_tts(analysis_results["Final Sentiment Analysis"], f"{company_name}_report_hindi.mp3")
    analysis_results["Audio"] = hindi_tts
    
    return {"Company": company_name, "Articles": articles_data, **analysis_results}
