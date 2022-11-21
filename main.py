from discover.discover import *

#TODO: 
#take vid ids from recent activity and call relatedVids with VIDs
#download videos
#convert to barcode
#discovery flow plan
#1. get channel stats
#2. get recent vids
#3. get related vids
#4. get channel subscriptions
#5. get featured channels
#6. get channel stats for each channel
#7. get recent vids for each channel

# given a list of video ids, download videos using pytube
from pytube import YouTube as yt

def download_videos(video_ids):
  for video_id in video_ids:
    download_video(video_id)

def download_video(video_id):
  try:
    yt('https://www.youtube.com/watch?v=' + video_id).streams.filter(res="144p").first().download()
  except:
    print("error: video not found")

def main():
  channel_id = 'UC3prwMn9aU2z5Y158ZdGyyA'
  # channel_id = "UCxeOc7eFxq37yW_Nc-69deA"
  video_id = "g7o2Rr1dsXQ"
  # videos = discover_videos(video_id)
  # save_video_to_csv(videos)
  # read videos from csv
  videos = pd.read_csv('videos_2022-11-21_104708.csv')
  download_videos(videos['id'].values)

if __name__ == "__main__":
  main()