from django.urls import path

<<<<<<< HEAD
from .views import SpaceView, LikeView

urlpatterns = [
    path("/main", SpaceView.as_view()),
    path("/<int:space_id>/like", LikeView.as_view())
=======
from .views import SpaceView, SpaceDetailView

urlpatterns = [
    path("/main", SpaceView.as_view()),
    path("/<int:space_id>", SpaceDetailView.as_view()),
>>>>>>> 26e4b9f020ad39072dd558a1ba75469b824e73bb
]
