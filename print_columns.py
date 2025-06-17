import pandas as pd

# Load the CSV file
df = pd.read_csv('categorized_conversations.csv')

# Print all column names
print(df.columns.tolist())
