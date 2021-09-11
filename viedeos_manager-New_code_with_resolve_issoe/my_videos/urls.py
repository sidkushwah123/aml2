from django.urls import path
from . import views

urlpatterns = [
    path('', views.MyVideosView.as_view(),name="my_videos"),
    path('<slug:types>', views.MyVideosView.as_view(),name="my_videos"),
    path('remove-video/<slug:video_id>', views.RemoveVIdeo, name="remove_video"),
]