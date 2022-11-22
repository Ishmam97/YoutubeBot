from pytube import YouTube as yt
# given a list of video ids, download videos using pytube
def download_videos(video_ids):
  for video_id in video_ids:
    download_video(video_id)
#download videos
def download_video(video_id):
  try:
    yt('https://www.youtube.com/watch?v=' + video_id).streams.filter(res="144p").first().download()
  except:
    print("error: video not found")