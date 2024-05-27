from db_config import engine
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# Load news data into a DataFrame
news_data = pd.read_sql('SELECT * FROM news_data', engine)

# Convert publish_date to date only (drop the time part)
news_data['publish_date'] = pd.to_datetime(news_data['publish_date']).dt.date

# Aggregate sentiment scores by date
daily_sentiment = news_data.groupby('publish_date')['sentiment'].mean().reset_index()
daily_sentiment.columns = ['date', 'average_sentiment']
#print("Daily Sentiment:\n", daily_sentiment.head())

# Load stock data into a DataFrame
stock_data = pd.read_sql('SELECT * FROM stock_data', engine)

# Ensure date column in stock data is in date format
stock_data['date'] = pd.to_datetime(stock_data['date']).dt.date

# Verify that both dataframes have overlapping dates
#print("Stock Data Dates:\n", stock_data['date'].unique())
#print("News Data Dates:\n", daily_sentiment['date'].unique())

# Merge stock data with daily sentiment scores
combined_data = pd.merge(stock_data, daily_sentiment, on='date', how='left')
#print("Combined Data:\n", combined_data.head())

# Check for missing sentiment values
missing_sentiment = combined_data[combined_data['average_sentiment'].isnull()]
#print("Missing Sentiment Data:\n", missing_sentiment)

# Select features and target variable
features = ['volume', 'average_sentiment']
X = combined_data[features]
y = combined_data['price']

# Fill missing sentiment values with 0
X['average_sentiment'].fillna(0, inplace=True)

# Display features and target
print("Features (X):\n", X.head())
print("Target (y):\n", y.head())

# Split the data
if len(X) > 1:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print("Training and Testing Sets Shapes:\n", X_train.shape, X_test.shape, y_train.shape, y_test.shape)
else:
    print("Not enough data to split into training and testing sets.")

# Initialize and train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"MSE: {mse}, R2: {r2}")

# Plot actual vs predicted stock prices
plt.figure(figsize=(12, 6))
plt.plot(y_test.index, y_test, label='Actual')
plt.plot(y_test.index, y_pred, label='Predicted', alpha=0.7)
plt.xlabel('Date')
plt.ylabel('Stock Price')
plt.title('Stock Price Prediction')
plt.legend()
plt.show()