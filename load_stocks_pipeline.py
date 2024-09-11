import http.client
import os
import json
from dotenv import load_dotenv
from db_operations import store_stock_data

# Load environment variables from .env file
load_dotenv()
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')
RAPIDAPI_PATH = os.getenv("RAPIDAPI_PATH")
RAPIDAPI_HOST = os.getenv('RAPIDAPI_HOST')

def fetch_stock_data():
    conn = http.client.HTTPSConnection(RAPIDAPI_HOST)
    headers = {
        'x-rapidapi-key': RAPIDAPI_KEY,
        'x-rapidapi-host': RAPIDAPI_HOST
    }
    
    conn.request("GET", RAPIDAPI_PATH, headers=headers)
    res = conn.getresponse()
    data = res.read()
    stock_data = json.loads(data.decode("utf-8"))
    for stock in stock_data:
        stock['volume'] = int(stock['volume'].replace(',', ''))
    return stock_data

if __name__ == "__main__":
    try:
        stock_data = fetch_stock_data()[0]  # Assuming the API returns a list of stocks
        store_stock_data(stock_data)
        #print("Stock data fetched and stored successfully.")
    except Exception as e:
        print(f"Error fetching or storing stock data: {e}")
