"""
CS299 Project 4
Data collection using YouTube API to automate search queries.
Authors: Elizabeth Huang
Last Modified: 10/25
"""

import googleapiclient.discovery
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Access environment variables
YT_API = os.getenv('YT_API')
OAUTH_SECRET = os.getenv('OAUTH_SECRET')

# API information
api_service_name = "youtube"
api_version = "v3"

# API client
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey = YT_API)

request = youtube.search().list(
    part="id,snippet",
    # publishedAt ="",
    type="video",
    q="call of duty", #query or search term goes here
    videoDuration="short",
    # videoDefinition="",
    maxResults=5,
)
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