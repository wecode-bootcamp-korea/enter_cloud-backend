from django.urls import path

from .views import ReviewView, ReviewCardView

urlpatterns = [
    path("", ReviewCardView.as_view()), 
    path("/<int:space_id>", ReviewView.as_view())
]
