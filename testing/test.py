import googleapiclient.discovery
import os
from dotenv import load_dotenv
import requests
from collections import Counter
import pandas as pd
import time
import concurrent.futures
import json

# Load .env file
load_dotenv()

# Access environment variables
YT_API = os.getenv('YT_API')

# API information
api_service_name = "youtube"
api_version = "v3"

# API client
youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=YT_API)

# Function to get video transcriptions (placeholder function)
def get_transcription(video_id):
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

# Function to get related videos from current video
def get_related_videos(video_id, n=5):
    request = youtube.search().list(
        part="id,snippet",
        type="video",
        maxResults=n,
        relatedToVideoId=video_id
    )
    response = request.execute()
    video_ids = [item['id']['videoId'] for item in response['items']]
    return video_ids

# Function to perform BFS for alt-right keywords
def bfs_for_alt_right_keywords(start_video_id, alt_right_keywords, skip_words):
    queue = [(start_video_id, 0)]
    visited = set()
    while queue:
        current_video_id, path_length = queue.pop(0)
        if current_video_id in visited:
            continue
        visited.add(current_video_id)
        transcription = get_transcription(current_video_id)
        word_freq = count_word_frequencies([transcription], skip_words)
        if any(word in word_freq for word in alt_right_keywords):
            return current_video_id, path_length
        
        related_videos = get_related_videos(current_video_id)
        queue.extend([(video_id, path_length + 1) for video_id in related_videos])
        time.sleep(1)  # Avoid hitting rate limits
    return None, -1

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
        alt_right_match_video_id, path_length = bfs_for_alt_right_keywords(initial_video_id, alt_right_keywords, skip_words)
        if alt_right_match_video_id:
            results.append({
                'initial_video_id': initial_video_id,
                'alt_right_match_video_id': alt_right_match_video_id,
                'path_length': path_length
            })
    return results

# Function to process queries in parallel and save results to JSON file
def process_queries_in_parallel(queries, alt_right_keywords, skip_words, output_file):
    all_results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_query = {executor.submit(analyze_videos, query, alt_right_keywords, skip_words): query for query in queries}
        for future in concurrent.futures.as_completed(future_to_query):
            query = future_to_query[future]
            try:
                result = future.result()
                all_results.extend(result)
            except Exception as exc:
                print(f"{query} generated an exception: {exc}")

    # Convert results to DataFrame
    df = pd.DataFrame(all_results)

    # Save DataFrame to JSON file
    if not os.path.exists('collected_data'):
        os.makedirs('collected_data')
    df.to_json(os.path.join('collected_data', output_file), orient='records', lines=True, indent=4)

# Example usage
with open("keywords/alt-right.txt", "r") as file:
    alt_right_keywords = [line.strip() for line in file]
with open("keywords/skip_words.txt", "r") as file:
    skip_words = [line.strip() for line in file]
with open("keywords/gaming.txt", "r") as file:
    gaming_keywords = [line.strip() for line in file]

query_queue = gaming_keywords
process_queries_in_parallel(query_queue, alt_right_keywords, skip_words, 'results.json')
