import googleapiclient.discovery
import os
from dotenv import load_dotenv
import requests
from collections import Counter
import pandas as pd
import time

# Load .env file
load_dotenv()

# Access environment variables
YT_API = os.getenv('YT_API')
OAUTH_SECRET = os.getenv('OAUTH_SECRET')

# API information
api_service_name = "youtube"
api_version = "v3"

# API client
youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=YT_API)

# Function to get video transcriptions (placeholder function)
def get_transcription(video_id):
    # Use YouTube API to get captions/transcriptions (update with correct method)
    response = requests.get(f"https://www.youtube.com/api/timedtext?v={video_id}&lang=en")
    if response.status_code == 200:
        return response.text
    else:
        return ""

# Function to count word frequencies
def count_word_frequencies(transcriptions, skip_words):
    words = []
    for transcription in transcriptions:
        words.extend([word.lower() for word in transcription.split() if word.lower() not in skip_words])
    return Counter(words)

# Function to get 5 related videos from current video
def get_top_recommended_videos(video_id):
    request = youtube.search().list(
        part="id,snippet",
        relatedToVideoId=video_id,
        type="video",
        maxResults=5
    )
    response = request.execute()
    video_ids = [item['id']['videoId'] for item in response['items']]
    return video_ids

# Main function to perform the analysis
def analyze_videos(query, alt_right_keywords, skip_words):
    results = []
    request = youtube.search().list(
        part="id,snippet",
        type="video",
        q=query,
        videoCategoryId="20",  # Gaming category ID
        maxResults=5
    )
    response = request.execute()
    for item in response['items']:
        initial_video_id = item['id']['videoId']
        transcription = get_transcription(initial_video_id)
        word_freq = count_word_frequencies([transcription], skip_words)
        alt_word_freq = {word: freq for word, freq in word_freq.items() if word in alt_right_keywords}

        recommended_video_ids = get_top_recommended_videos(initial_video_id)
        for recommended_video_id in recommended_video_ids:
            recommended_transcription = get_transcription(recommended_video_id)
            recommended_word_freq = count_word_frequencies([recommended_transcription], skip_words)
            if recommended_word_freq == alt_word_freq:
                results.append({
                    'initial_video_id': initial_video_id,
                    'alt_right_match_video_id': recommended_video_id,
                    'iterations': recommended_video_ids.index(recommended_video_id) + 1
                })
                break
            time.sleep(1)  # Avoid hitting rate limits

    return results

# Example usage
alt_right_keywords = ["keyword1", "keyword2", "keyword3"]  # Replace with actual keywords
skip_words = ["the", "and", "is", "a", "an", "or", "but", "because", "in", "on", "at", "are", "do", "has", "this", "that", "these", "those"]
query = "call of duty"  # Example query

results = analyze_videos(query, alt_right_keywords, skip_words)
df = pd.DataFrame(results)
print(df)
