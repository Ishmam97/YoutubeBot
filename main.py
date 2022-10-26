from importlib.metadata import requires
from urllib import response
from dotenv import load_dotenv
import os

from googleapiclient.discovery import build

def main():
  load_dotenv()
  yt_api_key = os.getenv('YOUTUBE_API_KEY')
  
  channel_id = "UCxeOc7eFxq37yW_Nc-69deA"

  youtube = build('youtube', 'v3', developerKey=yt_api_key)
  

if __name__ == "__main__":
  main()