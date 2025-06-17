import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV
df = pd.read_csv('all_messages.csv')

# Change 'author_role' to any column you want to plot (e.g., 'category', 'author_name', etc.)
column = 'author_role'

# Count occurrences
counts = df[column].value_counts()

# Plot
plt.figure(figsize=(10, 6))
counts.plot(kind='bar', color='skyblue')
plt.title(f'Count by {column}')
plt.ylabel('Count')
plt.xlabel(column)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()