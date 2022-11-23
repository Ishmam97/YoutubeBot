from discover.discover import *
from utils.utils import *
import numpy as np
import pandas as pd

#TODO: 
#take vid ids from recent activity and call relatedVids with VIDs
#convert to barcode
#discovery flow plan
#1. get channel stats
#2. get recent vids
#3. get related vids
#4. get channel subscriptions
#5. get featured channels
#6. get channel stats for each channel
#7. get recent vids for each channel

def main():
  # channel_id = "UCxeOc7eFxq37yW_Nc-69deA"
  video_id = "CJ8y3hw6Bqo"
  # videos = discover_videos(video_id)
  # videos_file = save_video_to_csv(videos)
  videos = pd.read_csv('videos_2022-11-23_153226.csv')
  channels = videos['channelId'].values
  subscriptions, featured_channels = discover_channels(np.unique(channels))
  print(subscriptions)

if __name__ == "__main__":
  main()