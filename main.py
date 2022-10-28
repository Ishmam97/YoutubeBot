from dotenv import load_dotenv
import os
from pprint import pprint

from googleapiclient.discovery import build

#gets channel statistics
def get_channel_stats(youtube, channel_id):
  request = youtube.channels().list(
    part='statistics',
    id=channel_id
  )
  response = request.execute()

  return response

#gets latest videos of chanel
def get_channel_activities(youtube, channel_id):
  request = youtube.activities().list(
    part='snippet,contentDetails',
    channelId=channel_id,
    maxResults=15
  )
  response = request.execute()

  return response

#get latest video ids of channels
def get_recent_video_ids(youtube, channel_id):
  activities = get_channel_activities(youtube, channel_id)
  ids = []
  for activity in activities['items']:
    ids.append(activity['contentDetails']['upload']['videoId'])
  
  return ids

#given vid find related vids
def get_related_videos(youtube, video_id):
  request = youtube.search().list(
    part="snippet",
    relatedToVideoId=video_id,
    type="video"
  )
  response = request.execute()

  return response

#take vid ids from recent activity and call relatedVids with VIDs

def main():
  load_dotenv()
  yt_api_key = os.getenv('YOUTUBE_API_KEY')
  
  channel_id = "UCxeOc7eFxq37yW_Nc-69deA"
  video_id = "g7o2Rr1dsXQ"

  youtube = build('youtube', 'v3', developerKey=yt_api_key)

  # pprint(get_channel_activities(youtube, channel_id))
  # pprint(get_channel_stats(youtube, channel_id))
  # pprint(get_related_videos(youtube, video_id))
  print(get_recent_video_ids(youtube, channel_id))

if __name__ == "__main__":
  main()