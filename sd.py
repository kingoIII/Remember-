import pandas as pd
import matplotlib.pyplot as plt

# Path to your CSV file
csv_file = 'conversation_percentages.csv'  # Change if your file has a different name

# Read the CSV
df = pd.read_csv(csv_file)

# List your category columns (update if you add/remove categories)
categories = [
    "Biblia", "Música", "Matemáticas", "Filosofía", "Ciencia", "Estupideces"
]

# Calculate average percentage for each category
averages = df[categories].mean()

# Plot
plt.figure(figsize=(10, 6))
averages.plot(kind='bar', color='skyblue')
plt.title('Average Percentage per Category')
plt.ylabel('Average Percentage')
plt.xlabel('Category')
plt.ylim(0, 100)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()