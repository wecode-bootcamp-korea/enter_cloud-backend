from django.urls import path
from users.views import SignUpView, SignInView, UserLikeView, UserProfileView

urlpatterns = [
    path("/signup", SignUpView.as_view()),
    path("/signin", SignInView.as_view()),
    path("/profile", UserProfileView.as_view()),
    path("/likes", UserLikeView.as_view())
]
