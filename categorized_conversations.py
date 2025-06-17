import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn import linear_model


# Load your categorized CSV
df = pd.read_csv("categorized_conversations.csv")

# Print all column names to help you update your analysis scripts
print('Column names:')
print(df.columns.tolist())


# Add a message length column based on 'title' (or change to another text column if needed)
df['message_length'] = df['title'].astype(str).apply(len)

# Plot: count of each category
plt.figure(figsize=(10, 6))
df['category'].value_counts().plot(kind='bar', color='skyblue')
plt.xlabel("Category")
plt.ylabel("Count")
plt.title("Count of Messages per Category")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Plot: message length distribution
plt.figure(figsize=(10, 6))
df['message_length'].plot(kind='hist', bins=50, color='orange')
plt.xlabel("Message Length")
plt.title("Distribution of Message Lengths")
plt.tight_layout()
plt.show()

# Select available columns as features (update as needed)
feature_cols = ['create_time', 'update_time', 'is_archived', 'is_starred', 'conversation_origin', 'voice', 'async_status', 'is_do_not_remember', 'memory_scope', 'category']
cdf = df[feature_cols + ['message_length']]

# Visualize: plot one category vs message length
plt.scatter(cdf['Estupideces'], cdf['message_length'])
plt.xlabel("Estupideces (%)")
plt.ylabel("Message Length")
plt.show()

# Split into train/test
msk = np.random.rand(len(df)) < 0.8
train = cdf[msk]
test = cdf[~msk]

# Train a regression model to predict message length from selected features
regr = linear_model.LinearRegression()
x = np.asanyarray(train[feature_cols])
y = np.asanyarray(train[['message_length']])
regr.fit(x, y)
print('Coefficients:', regr.coef_)

# Test the model
y_hat = regr.predict(test[feature_cols])
x_test = np.asanyarray(test[feature_cols])
y_test = np.asanyarray(test[['message_length']])
print("Mean Squared Error (MSE): %.2f" % np.mean((y_hat - y_test) ** 2))
print('Variance score: %.2f' % regr.score(x_test, y_test))