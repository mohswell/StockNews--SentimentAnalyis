### Data Cleaning and Processing for stocks data
import pandas as pd
from db_config import engine, DB_TABLE

# Load news data from MySQL table
news_data = pd.read_sql(f'SELECT * FROM {DB_TABLE}', engine)
print(news_data.isnull().sum())

# Extract word counts from the 'text' column
news_data['word_count'] = news_data['text'].apply(lambda x: len(x.split()))
print(news_data.head())

# Calculate rolling averages for 'price' and 'volume' columns
#stock_data['price_rolling_mean'] = stock_data['price'].rolling(window=7).mean()
#stock_data['volume_rolling_mean'] = stock_data['volume'].rolling(window=7).mean()

# Check the new features
#print(stock_data.head())