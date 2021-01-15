from django.urls import path

from .views import SpaceView

urlpatterns = [
    path("/main", SpaceView.as_view())
]
