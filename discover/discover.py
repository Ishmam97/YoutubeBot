from dotenv import load_dotenv
import os
from pprint import pprint
import pandas as pd
from datetime import datetime
from googleapiclient.discovery import build

#gets channel statistics
#uses channel id to retreive channel statistics as JSON/dict
load_dotenv()
yt_api_key = os.getenv('YOUTUBE_API_KEY')
youtube = build('youtube', 'v3', developerKey=yt_api_key)

def get_channel_stats(channel_id):
  request = youtube.channels().list(
    part='statistics',
    id=channel_id
  )
  response = request.execute()

  return response

#gets latest videos of channel
def get_channel_activities(channel_id):
  request = youtube.activities().list(
    part='snippet,contentDetails',
    channelId=channel_id,
    maxResults=15
  )
  response = request.execute()

  return response

#get latest video ids of channels
def get_recent_video_ids(channel_id):
  activities = get_channel_activities(channel_id)
  ids = []
  for activity in activities['items']:
    ids.append(activity['contentDetails']['upload']['videoId'])
  
  return ids

#given vid find related vids
def get_related_videos(video_id):
  request = youtube.search().list(
    part="snippet",
    relatedToVideoId=video_id,
    type="video",
    maxResults=50
  )
  response = request.execute()

  return response

# gets list of channels the target is subscribed to
def get_channel_subscriptions(channel_id):
  try:
    request = youtube.subscriptions().list(
      part='snippet',
      channelId=channel_id,
    )
    response = request.execute()

    subscribed_channels = []

    for item in response['items']:
      subscribed_channels.append(item['snippet']['resourceId']['channelId'])

    return subscribed_channels
    
  except:
    print("error: subscription list is private")
    return []

  return response

# gets list of featured channels on the target channel
def get_featured_channels(channel_id):
  request = youtube.channelSections().list(
    part='contentDetails',
    channelId=channel_id
  )
  response = request.execute()
  featured_channels = []
  for item in response['items']:
    if 'contentDetails' in item:
      if 'channels' in item['contentDetails']:
        for channel in item['contentDetails']['channels']:
          featured_channels.append(channel)

  return featured_channels

def discover_videos(video_id):
  #keyword extraction
  #targetted search
  related = get_related_videos(video_id)
  videos = []
  crawlTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  for item in related['items']:
    video = {}
    video['id'] = item['id']['videoId']
    video['channelId'] = item['snippet']['channelId']
    video['title'] = item['snippet']['title']
    video['description'] = item['snippet']['description']
    video['publishedAt'] = item['snippet']['publishedAt']
    video['thumbnail'] = item['snippet']['thumbnails']['medium']['url']
    video['crawlTime'] = crawlTime
    videos.append(video)
  print(f'{len(videos)} videos discovered')

  return videos

#function for saving video information as csv/to database
def save_video_to_csv(videos):
  time_now = datetime.now().strftime("%Y-%m-%d_%H%M%S")
  file_name = f'videos_{time_now}.csv'
  pd.DataFrame(videos).to_csv(file_name, index=False)
