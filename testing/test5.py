"""
CS299 Project 4
Data collection using YouTube API to automate search queries.
Authors: Elizabeth Huang, Brooke Bao
Last Modified: 11/06/2024
"""

import requests
import pandas as pd
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Access environment variables
API_KEY = os.getenv('YT_API3')
SEARCH_URL = 'https://www.googleapis.com/youtube/v3/search'

# Parameters for retrieving gaming videos
params = {
    'part': 'snippet',
    'type': 'video',                # Focus on videos only
    'videoCategoryId': '20',        # Category ID for "Gaming"
    'maxResults': 1,                # Retrieve only the top result per request
    'order': 'viewCount',           # Order by most viewed
    'key': API_KEY
}

data = []

def get_info(item):
    videoID = item['id']['videoId']
    snippet = item['snippet']
    channelID = snippet['channelId']
    title = snippet['title']
    description = snippet['description']
    liveBroadcastContent = snippet['liveBroadcastContent']
    channelTitle = snippet['channelTitle']
    publishTime = snippet['publishTime']
    return [videoID, channelID, title, description, liveBroadcastContent, channelTitle, publishTime]

# Read search queries from 'gaming.txt'
with open('keywords/alt-right.txt', 'r') as file:
    search_queries = [line.strip() for line in file]

def search_videos(query):
    params['q'] = query
    response = requests.get(SEARCH_URL, params=params)
    result = response.json()
    
    if 'error' in result:
        print("Error:", result['error'])
        return []
    
    # Return only the top result
    return result.get('items', [])[:1]

# Search for each query and collect data
for query in search_queries:
    try:
        results = search_videos(query)
        for item in results:
            info = get_info(item)
            data.append(info)
        
        # Save interim results to ensure data is not lost
        interim_df = pd.DataFrame(data, columns=['videoID', 'channelID', 'title', 'description', 'liveBroadcastContent', 'channelTitle', 'publishTime'])
        interim_df.to_csv("gaming_videos_batch_11-06-2024.csv", index=False)
    except Exception as e:
        print(f"An error occurred with query '{query}': {e}")

# Final DataFrame creation and saving to ensure completeness
df = pd.DataFrame(data, columns=['videoID', 'channelID', 'title', 'description', 'liveBroadcastContent', 'channelTitle', 'publishTime'])
print(df.head())

# Save the final DataFrame to a CSV file
df.to_csv("gaming_videos_batch_11-06-2024.csv", index=False)

# Verify results
print(f"Total videos retrieved: {len(df)}")