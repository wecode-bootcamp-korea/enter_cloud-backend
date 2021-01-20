from django.urls import path

from .views import SpaceCardView, SpaceDetailView, LikeView, SpaceListView

urlpatterns = [
    path("/main", SpaceCardView.as_view()),
    path("/<int:space_id>", SpaceDetailView.as_view()),
    path("/<int:space_id>/like", LikeView.as_view()),
    path("/search", SpaceListView.as_view())
]
