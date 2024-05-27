import requests
import pandas as pd
import os
from dotenv import load_dotenv
from db_operations import store_news_data

# Load environment variables from .env file
load_dotenv()
API_URL = os.getenv('NEWS_API_URL')

# Fetch news from the NewsWorld API
def fetch_news_data():
    response = requests.get(API_URL)
    
    if response.status_code == 200:
        data = response.json()
        # Try different possible keys
        if 'news' in data:
            return data['news']
        elif 'News' in data:
            return data['News']
        else:
            raise KeyError("The expected key 'news' or 'News' was not found in the response.")
    else:
        response.raise_for_status()

if __name__ == "__main__":
    try:
        news_data = fetch_news_data()
        store_news_data(news_data)
        print("News data fetched and stored successfully.")
    except Exception as e:
        print(f"Error fetching or storing news data: {e}")