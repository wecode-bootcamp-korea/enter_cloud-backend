from django.http import JsonResponse

from django.views import View
from spaces.models import Space
from reviews.models import Review

class ReviewView(View):
    def get(self, request, space_id):
        space = Space.objects.get(id = space_id)
        reviews = space.review_set.all().select_related("user")
        review_data = [
            {
                "content"           :review.content,
                "user_nickname"     :review.user.nickname,
                "user_avatar_image" :review.user.avatar_image,
                "rating"            :review.rating,
                "created_at"        :review.created_at
            }
            for review in reviews
        ]
        self.review_list = review_data
        return JsonResponse({"review_data":review_data}, status = 200)

