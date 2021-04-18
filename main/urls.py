from django.urls import path
from . import views

#33389
app_name = "main"

urlpatterns = [
	
	path('', views.videos, name="videos"),
	path('play-video', views.play_video, name="play-video"),

	]