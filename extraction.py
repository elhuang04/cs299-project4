"""
CS299 Project 4
Clean and process data collected from YouTube API.
Extract relevant entities.
Steps:
    1. Merges all csv outputs from data collection process.
    2. Turns alt-right search result videos into a separate dataframe.
    3. Uses NLP library to only extract key entities (nouns, verbs) and check that none of these extracted words are listed in 'skip_words.txt'.
    4. Gets all keywords already in "keywords/alt-right.txt" and concatenates those keywords with the extracted ones above.
    5. Count the number of alt-right keywords in each video's transcript
    6. Parallel processing to count keywords in each video and update the DataFrame
    7. Update combined_df with keyword counts
Authors: Elizabeth Huang
Last Modified: 11/06/2024
"""
import os
import pandas as pd
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from concurrent.futures import ThreadPoolExecutor

# Step 1: Merge all CSV outputs from data collection process
main_dir = "collected_data"
folder_paths = [os.path.join(main_dir, folder) for folder in os.listdir(main_dir) if os.path.isdir(os.path.join(main_dir, folder))]
all_data = []
for folder_path in folder_paths:
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            df = pd.read_csv(file_path)
            df = df[['videoID', 'channelID', 'title', 'description', 'liveBroadcastContent', 'channelTitle', 'publishTime']]
            all_data.append(df)
combined_df = pd.concat(all_data, ignore_index=True).drop_duplicates()
combined_df['description'] = combined_df['description'].fillna("")

# Step 2: Turn alt-right search result videos into a separate dataframe
df_alt_right = pd.read_csv('keywords/test_batch_alt-right.csv')

# Step 2.5: Helper function to get transcripts
def get_transcript(video_id):
    try:
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([entry['text'] for entry in transcript_data]).lower()
    except NoTranscriptFound:
        return ""
    except Exception as e:
        return ""

# Step 3: Extract key entities (nouns, verbs) from video transcripts
import spacy

nlp = spacy.load("en_core_web_sm")
with open('keywords/skip_words.txt', 'r') as file:
    skip_words = {line.strip().lower() for line in file}

def extract_nouns_verbs(df):
    combined_text = " ".join(get_transcript(video) for video in df["videoID"])
    doc = nlp(combined_text)
    return [token.text for token in doc if token.text.lower() not in skip_words]

extracted_keywords = set(extract_nouns_verbs(df_alt_right))

# Step 4: Get all keywords from "keywords/alt-right.txt" and combine with extracted entities
with open('keywords/alt-right.txt', 'r') as file:
    existing_keywords = {line.strip().lower() for line in file}
all_keywords = existing_keywords.union(extracted_keywords)

# Step 5: Preprocess keywords and combine them into a single string
all_keywords_text = " ".join(all_keywords)

# Step 6: Compute Cosine Similarity between video transcripts and the combined keyword list
def compute_cosine_similarity(video_id):
    transcript = get_transcript(video_id)
    if transcript:
        # Combine the transcript and the all_keywords_text for vectorization
        documents = [transcript, all_keywords_text]
        
        # Initialize the TF-IDF vectorizer
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(documents)
        
        # Calculate cosine similarity between the transcript and the combined keyword list
        cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        return cosine_sim[0][0]  # Extract the cosine similarity score
    return 0.0  # Return 0 if no transcript is available

# Step 7: Parallel processing to compute similarity for each video and store results
similarity_scores = []
with ThreadPoolExecutor() as executor:
    for idx, result in enumerate(executor.map(lambda video_id: (video_id, compute_cosine_similarity(video_id)), combined_df['videoID']), 1):
        similarity_scores.append(result)
        if idx % 100 == 0:
            print(f"Processed {idx} videos")

# Step 8: Update combined_df with similarity scores
similarity_dict = dict(similarity_scores)
combined_df['alt_right_similarity_score'] = combined_df['videoID'].map(similarity_dict)

# Display the updated DataFrame and save to CSV
print(combined_df[['videoID', 'channelID', 'title', 'description', 'liveBroadcastContent', 'channelTitle', 'publishTime', 'alt_right_similarity_score']].head())
combined_df.to_csv("analysis.csv", index=False)
