from django.urls import path, include

urlpatterns = [
    path('user', include('users.urls')),
    path("spaces", include("spaces.urls")),
    path("reviews", include("reviews.urls")),
    path("reservation", include("reservations.urls"))
]
