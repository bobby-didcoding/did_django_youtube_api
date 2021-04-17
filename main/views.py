from django.shortcuts import render
from django.conf import settings

from .mixins import YouTube

'''
Basic view for displaying videos 
'''
def videos(request):

	videos = YouTube().get_data()

	context = {"videos": videos}
	return render(request, 'main/videos.html', context)


'''
Basic view for showing a video in an iframe 
'''
def play_video(request):

	vid_id = request.GET.get("vid_id")

	vid_data = YouTube(vid_id = vid_id).get_video()

	context = {
		"vid_data": vid_data,
	}
	return render(request, 'main/play_video.html', context)
