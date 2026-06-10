from django.contrib import admin
from django.urls import path, include

# urls.py — tells Django which URLs to respond to and which view function to run for each URL
# path — defines a URL pattern and the view function to run when that URL is accessed
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('exclusions.urls')),
]

# If it starts with admin, send it to the admin system, otherwise send it to the exclusions app to figure out what to do.