from django.conf import settings
import requests
import json
import os

import googleapiclient.discovery
import googleapiclient.errors



def title_formatting(title):

	if len(title) >= 30:
		return f'{title[0:26]}...'
	else:
		return title



'''
Retreives video data from a YouTube channel
'''
class YouTube:

	def __init__(self, *args, **kwargs):

		#vid_id for get_video
		self.vid_id = kwargs.get("vid_id")

		self.api_service_name = settings.API_SERVICE_NAME #This is 'youtube' for this tutorial
		self.api_version = settings.API_VERSION #This is 'v3' for this tutorial
		self.developer_key = settings.GOOGLE_API_KEY # make sure you have Youtube APIS enabled in Google console
		self.channel_id = settings.CHANNEL_ID # This will be your own channel ID for this tutorial


		#https://github.com/googleapis/google-api-python-client/blob/master/docs/README.md
		#https://googleapis.github.io/google-api-python-client/docs/epy/googleapiclient.discovery-module.html#build

		# Construct a Resource object for interacting with an API. The serviceName and
		# version are the names from the Discovery service.

		self.youtube = googleapiclient.discovery.build(
	        self.api_service_name,
	        self.api_version,
	        developerKey=self.developer_key
	        )

	def get_data(self):


		#get playlists for channelId
		playlist_request = self.youtube.playlists().list(
			part="snippet,contentDetails",
			channelId=self.channel_id,
			)
		
		playlist_response = playlist_request.execute()

		#list of playlists
		playlists = [p["id"] for p in playlist_response["items"]]

		nextPageToken = None

		videos = []
		data = []
		
		while True:
			
			#make another request for playlist data (max results for page 1 is 50) 
			for pl in playlists:
				playlist_items_request = self.youtube.playlistItems().list(
					part="contentDetails",
					playlistId=pl,
					maxResults=50,
					pageToken=nextPageToken
					)
				playlist_items_response = playlist_items_request.execute()

				#append video ID to list
				for item in playlist_items_response["items"]:
					videos.append(item["contentDetails"]["videoId"])
			
			#make another request to get video specific infomation
			video_request = self.youtube.videos().list(
				part="contentDetails,snippet,player",
				id=",".join(videos)
				)
			video_response = video_request.execute()

			for item in video_response["items"]:

				#create dict for each video and append to data list
				vid_data = {
					"id": item["id"],
					"title":item["snippet"]["title"],
					"title_formatted":title_formatting(item["snippet"]["title"]),
					"description":item["snippet"]["description"],
					"thumbnail":item["snippet"]["thumbnails"]["medium"]["url"],
					"iframe":item["player"]["embedHtml"],
				}

				data.append(vid_data)

			
			#get next page token from request - break while loop if there aren't anymore pages
			nextPageToken = playlist_response.get("nextPageToken")
			if not nextPageToken:
				break

		return data

	def get_video(self):


		#retrieve data for 1 x video. This is similar to the get_data method	
		video_request = self.youtube.videos().list(
			part="contentDetails,snippet,player",
			id=self.vid_id
			)
		
		video_response = video_request.execute()

		item = video_response["items"][0]

		vid_data = {
			"id": item["id"],
			"title":item["snippet"]["title"],
			"description":item["snippet"]["description"],
			"iframe":item["player"]["embedHtml"],
		}

		return vid_data
