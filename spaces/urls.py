from django.urls import path

from .views import SpaceCardView, SpaceDetailView, LikeView
urlpatterns = [
    path("/main", SpaceCardView.as_view()),
    path("/<int:space_id>", SpaceDetailView.as_view()),
    path("/<int:space_id>/like", LikeView.as_view()),
]
