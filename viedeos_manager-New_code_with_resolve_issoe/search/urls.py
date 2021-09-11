from django.urls import path
from . import views

urlpatterns = [
    path('', views.SearchView.as_view(),name="search"),
    path('search_item', views.search_item  ,name="search_item"),
]