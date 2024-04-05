from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dataset', views.dataset, name='dataset'),
    path('vectordataset', views.vectordataset, name='vectordataset')
]