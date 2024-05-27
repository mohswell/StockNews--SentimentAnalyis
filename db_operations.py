import os
from sqlalchemy import create_engine, Table, Column, Integer, String, DECIMAL, MetaData, DateTime
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import datetime

# Get database credentials from environment variables
load_dotenv()
DB_USER = os.getenv('DB_USER') 
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

# Define database connection
DATABASE_URL = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Define metadata
metadata = MetaData()

# Define news data table
news_data_table = Table('news_data', metadata,
    Column('id', Integer, primary_key=True),
    Column('article_id', Integer, nullable=False),
    Column('title', String(255), nullable=False),
    Column('text', String, nullable=False),
    Column('url', String(255)),
    Column('publish_date', DateTime, nullable=False),
    Column('author', String(255)),
    Column('language', String(10)),
    Column('source_country', String(10)),
    Column('sentiment', DECIMAL(3, 2), nullable=False)
)

# Define stocks data table
stocks_data_table = Table('stock_data', metadata,
    Column('id', Integer, primary_key=True),
    Column('ticker', String(255), nullable=False),
    Column('name', String(255), nullable=False),
    Column('volume', Integer, nullable=False),  
    Column('price', DECIMAL(10, 2), nullable=False),
    Column('change', DECIMAL(5, 2), nullable=False),
    Column('date', DateTime)  # Adding a date column if needed
)

# Create tables in the database
metadata.create_all(engine)

def store_news_data(news_data):
    # Insert data into the database
    for news in news_data:
        news_record = {
            'article_id': news['id'],
            'title': news['title'],
            'text': news['text'],
            'url': news['url'],
            'publish_date': news['publish_date'],
            'author': ', '.join(news['authors']) if 'authors' in news else news['author'],
            'language': news['language'],
            'source_country': news['source_country'],
            'sentiment': news['sentiment']
        }
        session.execute(news_data_table.insert().values(news_record))
    session.commit()
    

def store_stock_data(stock_data):
    # Insert data into the database
    stock_record = {
        'ticker': stock_data['ticker'],
        'name': stock_data['name'],
        'volume': stock_data['volume'],
        'price': stock_data['price'],
        'change': stock_data['change'],
        'date': datetime.datetime.now()
    }
    session.execute(stocks_data_table.insert().values(stock_record))
    session.commit()