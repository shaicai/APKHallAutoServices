from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('apkhall/', views.apkhall),
    path('uploadFile/', views.upload_file),
]
