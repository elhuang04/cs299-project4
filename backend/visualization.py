import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# Load data
data = pd.read_csv("classified_video_titles.csv")

# Calculate and print the average similarity score across all gaming videos
average_similarity_score = data['alt_right_similarity_score'].mean()
print("The average similarity score across all gaming videos was:", average_similarity_score)

# Calculate the average similarity score for each category
category_avg_scores = data.groupby('predicted_category')['alt_right_similarity_score'].mean()

# Find the category with the highest average similarity score
top_category = category_avg_scores.idxmax()
top_category_score = category_avg_scores.max()

# Find the row with the highest similarity score
max_similarity_row = data.loc[data['alt_right_similarity_score'].idxmax()]

# Get the category and the score
max_category = max_similarity_row['predicted_category']
max_score = max_similarity_row['alt_right_similarity_score']

# Print the highest single similarity score and the corresponding category
print(f"The sub-category with the highest average similarity score is: {top_category} with an average score of {top_category_score}")
print(f"The sub-category with the highest single similarity score is: {max_category} with a score of {max_score}")

# Count the number of videos in the 'Minecraft Hacks' sub-category
minecraft_hacks_count = data[data['predicted_category'] == 'Minecraft Hacks'].shape[0]
print(f"The number of videos in the 'Minecraft Hacks' sub-category is: {minecraft_hacks_count}")

# Verify the maximum similarity score
print(f"Maximum similarity score in the dataset is: {data['alt_right_similarity_score'].max()}")

print(data.nlargest(5, 'alt_right_similarity_score')[['videoID', 'title', 'alt_right_similarity_score']])


# Convert publishTime to datetime and extract year
data['publishTime'] = pd.to_datetime(data['publishTime'])
data['publishYear'] = data['publishTime'].dt.year

# Set up visual style
sns.set(style="whitegrid")

# 1. Distribution of alt_right_similarity_score
plt.figure(figsize=(10, 6))
sns.histplot(data['alt_right_similarity_score'], bins=30, kde=True, color="skyblue")
plt.title("Distribution of Alt-right Similarity Score")
plt.xlabel("Alt-right Similarity Score")
plt.ylabel("Frequency")
plt.show()

# 2. Bar Chart for Predicted Categories
plt.figure(figsize=(12, 8))
sns.countplot(y="predicted_category", data=data, order=data['predicted_category'].value_counts().index)
plt.title("Predicted Category Distribution")
plt.xlabel("Count")
plt.ylabel("Predicted Category")
plt.show()

# 3. Publish Year Trend
plt.figure(figsize=(10, 6))
yearly_trend = data['publishYear'].value_counts().sort_index()
sns.lineplot(x=yearly_trend.index, y=yearly_trend.values, marker="o", color="coral")
plt.title("Trend of Video Uploads Over Years")
plt.xlabel("Year")
plt.ylabel("Number of Videos Published")
plt.show()

# 4. Publish Year vs Alt-Right Similarity Score
plt.figure(figsize=(10, 6))
alt_right_yearly_trend = data.groupby('publishYear')['alt_right_similarity_score'].mean()
sns.lineplot(x=alt_right_yearly_trend.index, y=alt_right_yearly_trend.values, marker="o", color="teal")
plt.title("Yearly Trend of Alt-right Similarity Score Over Time")
plt.xlabel("Year")
plt.ylabel("Average Alt-right Similarity Score")
plt.show()

# 5. Category vs Alt-right Similarity Score
plt.figure(figsize=(12, 8))
sns.boxplot(x="predicted_category", y="alt_right_similarity_score", data=data, palette="coolwarm")
plt.title("Category vs Alt-right Similarity Score")
plt.xlabel("Predicted Category")
plt.ylabel("Alt-right Similarity Score")
plt.xticks(rotation=45, ha="right")  # Rotate x labels for better readability
plt.show()

# 6. Category vs Alt-right Similarity Score (Violin Plot)
plt.figure(figsize=(12, 8))
sns.violinplot(x="predicted_category", y="alt_right_similarity_score", data=data, palette="muted")
plt.title("Category vs Alt-right Similarity Score (Violin Plot)")
plt.xlabel("Predicted Category")
plt.ylabel("Alt-right Similarity Score")
plt.xticks(rotation=45, ha="right")  # Rotate x labels for better readability
plt.show()


# 7. Top 10 Categories vs Alt-right Similarity Score (Boxplot)
top_10_categories = data['predicted_category'].value_counts().head(10).index
top_10_data = data[data['predicted_category'].isin(top_10_categories)]

plt.figure(figsize=(12, 8))
sns.boxplot(x="predicted_category", y="alt_right_similarity_score", data=top_10_data, palette="coolwarm")
plt.title("Top 10 Categories vs Alt-right Similarity Score (Boxplot)")
plt.xlabel("Predicted Category")
plt.ylabel("Alt-right Similarity Score")
plt.xticks(rotation=45, ha="right")  # Rotate x labels for better readability
plt.show()

# 8. Top 10 Categories vs Alt-right Similarity Score (Violin Plot)
plt.figure(figsize=(12, 8))
sns.violinplot(x="predicted_category", y="alt_right_similarity_score", data=top_10_data, palette="muted")
plt.title("Top 10 Categories vs Alt-right Similarity Score (Violin Plot)")
plt.xlabel("Predicted Category")
plt.ylabel("Alt-right Similarity Score")
plt.xticks(rotation=45, ha="right")  # Rotate x labels for better readability
plt.show()
