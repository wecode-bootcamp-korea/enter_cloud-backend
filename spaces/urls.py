from django.urls import path

from .views import SpaceCardView, SpaceDetailView

urlpatterns = [
    path("/main", SpaceCardView.as_view()),
    path("/<int:space_id>", SpaceDetailView.as_view()),
]
