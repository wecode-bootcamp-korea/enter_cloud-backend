from django.urls import path

from .views import ReservationView

urlpatterns = [
    path("/<int:detail_space_id>", ReservationView.as_view())
]
