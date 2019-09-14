from django.urls import path
from . import views

urlpatterns = [
    path(r'', views.search, name='search')
]
