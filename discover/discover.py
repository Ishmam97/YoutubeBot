from dotenv import load_dotenv
import os
from pprint import pprint
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

#given a list of channels, return a list of subscriptions and featured channels
def discover_channels(channels):
  subscriptions = []
  featured_channels = []

  for channel in channels:
    subs = get_channel_subscriptions(channel)
    featured = get_featured_channels(channel)
    #append if not empty
    if subs:
      subscriptions.append({channel:subs})
    if featured:
      featured_channels.append({channel:featured})

  return subscriptions, featured_channels


# returns array of comments 
def format_comment_response(response):
  comments = []
  for item in response['items']:
    comment = {}
    comment['video_id'] = item['snippet']['videoId']
    comment['id'] = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
    comment['comment'] = item['snippet']['topLevelComment']['snippet']['textOriginal']
    comment['likeCount'] =  item['snippet']['topLevelComment']['snippet']['likeCount']
    comment['lastUpdated'] = item['snippet']['topLevelComment']['snippet']['updatedAt']
    
    replycount = item['snippet']['totalReplyCount']
    
    comment['replyCount'] = replycount
   
    if replycount>0:
      replies = []      
      for reply in item['replies']['comments']:
        reply = reply['snippet']['textDisplay']
        replies.append(reply)

      comment['replies'] = replies

    comments.append(comment)
  return comments

#given a video id, return a list of comments
def get_comments(video_id):
  try:
    request = youtube.commentThreads().list(
        part="snippet,replies",
        textFormat="plainText",
        videoId=video_id,
        maxResults=100
    )
    response = request.execute()
  except Exception as e:
    print("error in retrieving comment for ", video_id)
    print(e)
    return
  
  comments = format_comment_response(response)

  if 'nextPageToken' in response:
    nextPageToken = response['nextPageToken']
  while nextPageToken:
    try:
      request = youtube.commentThreads().list(
        part="snippet,replies",
        textFormat="plainText",
        videoId=video_id,
        maxResults=100,
        pageToken=nextPageToken
      )
      response = request.execute()
    except Exception as e:
      print("error in retrieving comment for ", video_id)
      print(e)
      return

    #append comments frm response to comments
    comments += format_comment_response(response)

    if 'nextPageToken' in response:
      nextPageToken = response['nextPageToken']
    else:
      break

  return comments
  