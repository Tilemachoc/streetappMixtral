from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('get_response', views.get_response, name='get_response'),
    path('dataset', views.dataset, name='dataset'),
    path('vectordataset', views.vectordataset, name='vectordataset')
]