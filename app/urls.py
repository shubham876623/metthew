from os import name
from django.urls import path
from app import views

urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('getdata', views.getdata, name="getdata"),
    path('download_csv', views.get_csv, name="get_csv"),
    path("csv_created", views.CreateCSVFILE.as_view(), name="create_csv"),
]
