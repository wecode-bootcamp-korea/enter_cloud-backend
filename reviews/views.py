from django.http import JsonResponse, HttpResponse

from django.views import View
from spaces.models import Space
from reviews.models import Review

class ReviewView(View):
    def get(self, request, space_id):
        try:
            PAGE_SIZE       = 3
            page            = request.GET.get("page", 1)
            limit           = PAGE_SIZE * int(page)
            offset          = limit - PAGE_SIZE            
            space           = Space.objects.get(id = space_id)
            reviews         = space.review_set.all().select_related("user")
        
            if not reviews.exists():
                reviews = reviews[0:PAGE_SIZE]
            else:
                reviews = reviews[offset:limit]
                
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
            return JsonResponse({"review_data":review_data}, status = 200)
        except ValueError:
            return HttpResponse("QUERY_STRING_IS_NOT_INTEGER")
            
            
        
