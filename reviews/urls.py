from django.urls import path

from .views import ReviewView

urlpatterns = [
    path("/<int:space_id>", ReviewView.as_view())
]
