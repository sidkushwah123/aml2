from django.urls import path
from . import views

urlpatterns = [
    path('add-videos', views.VideosAddView.as_view(),name="add_videos"),
    path('get_sub_category', views.get_sub_category,name="get_sub_category"),
    path('add_video_info', views.add_video_info,name="add_video_info"),
    path('update-views/<slug:video_id>', views.UpdateVideoVIdesView,name="update_views"),
]