from discover.discover import *
from utils.utils import *
import pandas as pd
import glob
from utils.barcode import *


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
  video_id = "0CTp1a-aCUM"
  # videos = discover_videos(video_id)
  # videos_file = save_video_to_csv(videos)
  # print(videos_file)
  videos = pd.read_csv('./videos_2022-12-14_035622.csv')

  videos = videos.head(10)

  video_ids = videos['id'].tolist()

  # download_videos(video_ids)

  video_files = glob.glob('./videos/*.3gpp')

  run_videos_to_barcodes(video_files)


if __name__ == "__main__":
  main()