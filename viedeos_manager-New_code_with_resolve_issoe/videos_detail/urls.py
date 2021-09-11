from django.urls import path
from . import views

urlpatterns = [
    path('<slug:video_id>/<slug:video_slug>', views.VideosDetailView.as_view(),name="videos_detail"),
    
]