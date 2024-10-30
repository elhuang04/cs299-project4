"""
CS299 Project 4
Data collection using YouTube API to automate search queries.
Authors: Elizabeth Huang
Last Modified: 10/25
"""

import os
from dotenv import load_dotenv
import requests

# Load .env file
load_dotenv()

# Access environment variables
API_KEY = os.getenv('YT_API')
OAUTH_SECRET = os.getenv('OAUTH_SECRET')
SEARCH_URL = os.getenv('SEARCH_URL')

# API information
api_service_name = "youtube"
api_version = "v3"

# API client
params = {
    'part': 'snippet',
    'type': 'video',               # Focus on videos only
    'videoCategoryId': '20',        # Category ID for "Gaming"
    'maxResults': 50,               # Maximum results per request
    'order': 'viewCount',           # Optional: Order by most viewed
    'key': API_KEY
}

response = requests.get(SEARCH_URL, params=params)

"""
# to request id and snippet parts properties
request = youtube.channels().list(
    part="id,snippet"
)
"""

# Query execution
response = request.execute()
# Print the results
print(response)

#TODO: store data into json or csv files
#TODO: get recommendations and use BFS to crawl more videos