from dotenv import load_dotenv
import os
from pprint import pprint

from googleapiclient.discovery import build

def get_channel_stats(youtube, channel_id):
  request = youtube.channels().list(
    part='statistics',
    id=channel_id
  )
  response = request.execute()

  return response

def get_channel_activities(youtube, channel_id):
  request = youtube.activities().list(
    part='snippet,contentDetails',
    channelId=channel_id,
    maxResults=1
  )
  response = request.execute()

  return response

def main():
  load_dotenv()
  yt_api_key = os.getenv('YOUTUBE_API_KEY')
  
  channel_id = "UCxeOc7eFxq37yW_Nc-69deA"
  video_id = "g7o2Rr1dsXQ"

  youtube = build('youtube', 'v3', developerKey=yt_api_key)

  # pprint(get_channel_activities(youtube, channel_id))
  # pprint(get_channel_stats(youtube, channel_id))

if __name__ == "__main__":
  main()