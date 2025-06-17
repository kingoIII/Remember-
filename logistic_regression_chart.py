import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# Load the CSV
df = pd.read_csv('categorized_conversations.csv')

# Use 'title' length as a feature and 'category' as the target
# For binary classification, let's predict if category == 'Estupideces' (1) or not (0)
df['message_length'] = df['title'].astype(str).apply(len)
df['is_estupideces'] = (df['category'] == 'Estupideces').astype(int)

# Features and target
X = df[['message_length']]
y = df['is_estupideces']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train logistic regression
logreg = LogisticRegression()
logreg.fit(X_train, y_train)

# Predict
y_pred = logreg.predict(X_test)

# Print metrics
print('Accuracy:', accuracy_score(y_test, y_pred))
print('Confusion Matrix:\n', confusion_matrix(y_test, y_pred))
print('Classification Report:\n', classification_report(y_test, y_pred))

# Plot the probability curve
X_range = np.linspace(X['message_length'].min(), X['message_length'].max(), 300).reshape(-1, 1)
probs = logreg.predict_proba(X_range)[:, 1]

plt.figure(figsize=(10, 6))
plt.scatter(X['message_length'], y, alpha=0.2, label='Data')
plt.plot(X_range, probs, color='red', linewidth=2, label='Logistic Regression Curve')
plt.xlabel('Message Length (title)')
plt.ylabel('Probability of Estupideces')
plt.title('Logistic Regression: Probability of Estupideces by Message Length')
plt.legend()
plt.tight_layout()
plt.show()
