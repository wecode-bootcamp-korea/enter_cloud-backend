from django.urls import path

from .views import SpaceView, SpaceListView, SpaceDetailView

urlpatterns = [
    path("/main", SpaceView.as_view()),
    path("/<int:space_id>", SpaceDetailView.as_view()),
]
