from django.urls import path
from users.views import SignupView, SigninView, UserLikeView

urlpatterns = [
    path("/signup", SignupView.as_view()),
    path("/signin", SigninView.as_view()),
    path("/likes", UserLikeView.as_view())
]
