"""
CS299 Project 4
Data collection using YouTube API to automate search queries.
This script formats the results of gaming category search
results into a csv file usable for data extraction.

Authors: Elizabeth Huang, Brooke Bao
Last Modified: 11/06/2024
"""

import requests
import json
import pandas as pd
import concurrent.futures
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Access environment variables
API_KEY = os.getenv('YT_API')
SEARCH_URL = 'https://www.googleapis.com/youtube/v3/search'

# startmonth = '01'
# startdate = '01'
# startyear = '2000'
# endmonth = '07'
# enddate = '01'
# endyear = '2025'

# Parameters for retrieving gaming videos
params = {
    'part': 'snippet',
    'type': 'video',               # Focus on videos only
    'videoCategoryId': '20',        # Category ID for "Gaming"
    'maxResults': 50,               # Maximum results per request
    'order': 'viewCount',           # Optional: Order by most viewed
    # 'publishedAfter': f'{startyear}-{startmonth}-{startdate}T00:00:00Z',  # Example date
    # 'publishedBefore': f'{endyear}-{endmonth}-{enddate}T00:00:00Z',  # End date
    'key': API_KEY
}

all_videos = []
next_page_token = None

# Loop to handle pagination
results = []
while True:
    if next_page_token:
        params['pageToken'] = next_page_token
    response = requests.get(SEARCH_URL, params=params)
    results.append(response.json())
    all_videos.extend(results[-1].get('items', []))
    
    # Debugging: Check for errors in response
    if 'error' in results:
        print("Error:", results['error'])
        break

    # Check if there's a next page
    next_page_token = results[-1].get('nextPageToken')
    if not next_page_token:
        break  # Exit loop if there are no more pages

print(f"Total videos retrieved: {len(all_videos)}")

data = []

def get_info(item):
    videoID = item['id']['videoId']
    snippet = item['snippet']
    channelID = snippet['channelId']
    title = snippet['title']
    description = snippet['description']
    liveBroadcastContent  = snippet['liveBroadcastContent']
    channelTitle = snippet['channelTitle']
    publishTime = snippet['publishTime']
    info = [videoID, channelID, title, description, liveBroadcastContent, channelTitle, publishTime]
    data.append(info)
    # return videoID, channelID, title, description, liveBroadcastContent, channelTitle, publishTime

# Display video IDs and titles for gaming videos
for result in results:
   if 'items' in result:
      all_info = "get_info(item)"
      with concurrent.futures.ThreadPoolExecutor() as executor:
         [exec(all_info) for item in result['items']]

print(data)
df = pd.DataFrame(data, columns=['videoID', 'channelID', 'title', 'description', 'liveBroadcastContent', 'channelTitle', 'publishTime'])
print(df.head())
#videoId, channelId, title, description, liveBroadcastContent, channelTitle, publishTime
# df.to_csv(f'testing_{startyear}_{startmonth}_{startdate}.csv', index = 'false')
df.to_csv("test_batch_11-06-2024-run.csv")

# verify results
# print(len(df))