from django.urls import path

from .views import SpaceView, SpaceListView

urlpatterns = [
    path("/main", SpaceView.as_view()),
    path("/search", SpaceListView.as_view())
]
