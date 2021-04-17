# did_django_youtube_api
Django project that uses YouTubes APIs to retreive video data from a channel ID

1) cd to development directory
2) mkvirtualenv did_django_youtube_api
3) mkdir did_django_youtube_api
4) clone repository to new directory
5) pip install -r requirements.txt
6) Update settings.py with your email API information


GOOGLE_API_KEY = "XXX"

CHANNEL_ID = 'XXX'


7) python manage.py makemigrations
8) python manage.py migrate
9) python manage.py runserver
10) https://localhost:8000 - Bob's your uncle!! 

