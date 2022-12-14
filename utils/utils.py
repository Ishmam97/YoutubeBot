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
    #add file name and extension
    yt('https://www.youtube.com/watch?v=' + video_id).streams.filter(res="144p").first().download(output_path='./videos', filename=video_id+'.3gpp')
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
    if not G.has_node(child):
      G.add_node(child)
    if not G.has_edge(parent, child):
      G.add_edge(parent, child, color=color)
  return G

#add nodes to graph
#edges has format [{parent:[children]}]
def add_to_graph(graph, edges, color):
  for edge in edges:
    for parent, children in edge.items():
      for child in children:
        if not graph.has_node(child):
          graph.add_node(child)
        if not graph.has_edge(parent, child):
          graph.add_edge(parent, child, color=color)
  return graph

def print_graph(G):
  plt.figure(figsize=(12, 10), dpi=80)
  edges = G.edges()
  colors = [G[u][v]['color'] for u,v in edges]

  pos = nx.kamada_kawai_layout(G)
  nx.draw(G, pos, edge_color=colors, with_labels=False)
  plt.savefig("Graph.png", format="PNG")
  plt.show()