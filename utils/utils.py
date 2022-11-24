from pytube import YouTube as yt
import pandas as pd
from datetime import datetime
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

#function for saving video information as csv/to database
def save_video_to_csv(videos):
  time_now = datetime.now().strftime("%Y-%m-%d_%H%M%S")
  file_name = f'videos_{time_now}.csv'
  pd.DataFrame(videos).to_csv(file_name, index=False)
  return file_name

# make graph of channels

import networkx as nx
import matplotlib.pyplot as plt

def create_graph(parent, children, color):
  G = nx.DiGraph()
  G.add_node(parent)
  for child in children:
    G.add_node(child)
    G.add_edge(parent, child, color=color)
  return G