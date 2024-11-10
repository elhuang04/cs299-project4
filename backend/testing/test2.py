import googleapiclient.discovery
import os
from dotenv import load_dotenv
import requests
from collections import Counter
import pandas as pd
import time
import concurrent.futures
import json
from youtube_transcript_api import YouTubeTranscriptApi
import re

# STATIC GLOBALS
with open("keywords/alt-right.txt", "r") as file:
    alt_right_keywords = [line.strip() for line in file]
with open("keywords/skip_words.txt", "r") as file:
    skip_words = [line.strip() for line in file]
with open("keywords/gaming.txt", "r") as file:
    gaming_keywords = [line.strip() for line in file]


# Load .env file
load_dotenv()
YT_API = os.getenv('YT_API2')

api_service_name = "youtube"
api_version = "v3"
youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=YT_API)

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
        video_id = item['id']['videoId']
        print("Video ID:", video_id)  # Debugging

        # Get transcription
        transcription = str(YouTubeTranscriptApi.get_transcript(video_id))
        
        # Skip if no transcription available
        if not transcription:
            print(f"No transcription for video {video_id}.")
            continue

        # Save transcription to file
        save_transcription(video_id, transcription)

        # Count general and alt-right keyword frequencies
        general_freq = count_word_frequencies(transcription)
        print("PRINT DEBUG - IGNORE - Filtered General Words (excluding skip words):", general_freq)

        alt_right_freq = count_word_frequencies(transcription, alt_right_keywords)

        # Prepare data in specified format
        top_50_general = sorted(general_freq.items(), key=lambda x: x[1], reverse=True)[:50]
        top_50_general = [(word, round(freq / sum(general_freq.values()) * 100, 2)) for word, freq in top_50_general]
        
        top_5_alt_right = sorted(alt_right_freq.items(), key=lambda x: x[1], reverse=True)[:5]
        top_5_alt_right = [(word, round(freq / sum(alt_right_freq.values()) * 100, 2)) for word, freq in top_5_alt_right]

        result = {
            "videoID": video_id,
            "top_50_general_keywords": top_50_general,
            "query_used": query,
            "number_of_alt_right_keywords": len(alt_right_freq),
            "top_5_alt_right_keywords": top_5_alt_right
        }
        print(json.dumps(result, indent=4))  # Debugging

        results.append(result)
        
    return results

def process_queries_in_parallel(queries, alt_right_keywords, skip_words, max_queries=20):
    all_results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_query = {executor.submit(analyze_videos, query, alt_right_keywords, skip_words): query for query in queries[:max_queries]}
        for future in concurrent.futures.as_completed(future_to_query):
            query = future_to_query[future]
            try:
                result = future.result()
                all_results.extend(result)
            except Exception as exc:
                print(f"{query} generated an exception: {exc}")

    df = pd.DataFrame(all_results)
    print(df.columns)  # Debugging
    print(df.head())   # Debugging
    return df

def save_transcription(video_id, transcription):
    if not os.path.exists('transcriptions'):
        os.makedirs('transcriptions')
    with open(f'transcriptions/{video_id}.txt', 'w') as file:
        file.write(transcription)
    print(f"Transcription saved for video {video_id}.")

def count_word_frequencies(transcription, keywords=[], skip_words=skip_words):
    words = transcription.lower().split()
    # Filter out skip_words before counting keywords
    if len(keywords):
        filtered_words = [
            word for word in words 
            if word not in skip_words and re.match(r'^[A-Za-z]+$', word)
        ]

    else:
        # Count top 50 most frequent words, excluding skip_words
        filtered_words = [word for word in words if word not in skip_words]
        top_50_most_frequent = Counter(filtered_words).most_common(50)
        return top_50_most_frequent  # Return list of tuples for top 50 most frequent words
    return Counter(filtered_words)

results_df = process_queries_in_parallel(gaming_keywords, alt_right_keywords, skip_words, max_queries=20)

if not os.path.exists('collected_data'):
    os.makedirs('collected_data')
with open(os.path.join('collected_data', 'data.json'), 'w') as outfile:
    json.dump(results_df.to_dict(orient="records"), outfile, indent=4)
