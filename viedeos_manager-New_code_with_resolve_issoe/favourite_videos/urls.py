from django.urls import path
from . import views

urlpatterns = [
    # path('', views.MyVideosView.as_view(),name="my_videos"),
    path('add-remove/<slug:video_id>', views.updatefavourite_videos_list,name="update_favirate"),
    path('check-favirate/<slug:video_id>', views.Checkfavourite_videos_list,name="check_favirate"),
]