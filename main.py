from discover.discover import *
from utils.download import *

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
  channel_id = 'UC3prwMn9aU2z5Y158ZdGyyA'
  # channel_id = "UCxeOc7eFxq37yW_Nc-69deA"
  video_id = "BEWz4SXfyCQ"
  videos = discover_videos(video_id)
  download_videos(pd.DataFrame(videos)['id'].values[0:1])

if __name__ == "__main__":
  main()