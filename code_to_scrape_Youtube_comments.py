# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 11:19:06 2024

@author: giulia macis
"""

from googleapiclient.discovery import build 
import csv

def get_video_details(video_id, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.videos().list(
        part="snippet",
        id=video_id
    )
    response = request.execute()
    video_info = response['items'][0]['snippet']
    title = video_info['title']
    release_date = video_info['publishedAt']
    return title, release_date

# Function to get comments from a video
def get_youtube_comments(video_id, api_key, max_comments=10000):
    # Initialize the YouTube API client
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    # Get video details for title and release date
    title, release_date = get_video_details(video_id, api_key)
    
    # Placeholder for storing comment data
    comments = []
    next_page_token = None

    while len(comments) < max_comments:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            pageToken=next_page_token,
            maxResults=min(100, max_comments - len(comments)),
            textFormat="plainText"
        )

        response = request.execute()

        for item in response['items']:
            # Accessing snippet data for each comment
            comment_snippet = item['snippet']['topLevelComment']['snippet']

            # Extract required fields, including title and release date
            comment_data = {
                "URL": f"https://www.youtube.com/watch?v={video_id}",
                "title": title,  
                "releaseDate": release_date,  
                "author": comment_snippet['authorDisplayName'],
                "comment": comment_snippet['textDisplay'],
                "publishedTimeText": comment_snippet['publishedAt'],
                "replyCount": item['snippet']['totalReplyCount'],
                "voteCount": comment_snippet['likeCount']
            }
            comments.append(comment_data)

        # Check if there is another page of comments
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    return comments

#

URL=input('please insert URL ')
api_key = "AIzaSyCvbrfwXHXdRL7Ge8y1qIRyCsLElTdHk6w"
video_id = URL[32:]
comments = get_youtube_comments(video_id, api_key)
folder_path = r"C:/Users/giulia macis/Desktop/TEXT ANALYSIS/video project" ###insert the path of the folder you want
file_name = f"{folder_path}/youtube_comments_{video_id}.csv"

# Save comments to a CSV file
with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ["URL", "title", "releaseDate", "author", "comment", "publishedTimeText", "replyCount", "voteCount"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(comments)
