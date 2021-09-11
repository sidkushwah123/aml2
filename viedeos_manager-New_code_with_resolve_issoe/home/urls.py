from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(),name="home"),
    path('page/<slug:keyword>', views.PageContentView.as_view(), name='page_content'),
    path('send-mail', views.SendMailVIew,name="send_mail"),
]