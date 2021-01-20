from django.http        import JsonResponse
from django.db.models   import Max
from django.db import connection

from django.views       import View
from spaces.models      import Space
from reviews.models     import Review

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
            return JsonResponse({"message":"QUERY_STRING_IS_NOT_INTEGER"}, status = 400)
            
class ReviewCardView(View):
    def get(self, request):
        PRICE       = 5000
        PAGE_SIZE   = 6
        page        = request.GET.get("page", 1)
        limit       = PAGE_SIZE * int(page)
        offset      = limit - PAGE_SIZE 
        reviews = Review.objects.all().order_by("-created_at").select_related("space").prefetch_related("space__detailspace_set")
        reviews     = reviews[offset:limit]
        review_card = [
            {
                "name"      : review.space.name,
                "content"   : review.content,
                "rating"    : review.rating,
                "image_url" : review.space.main_image,
                "price"     : review.space.detailspace_set.all().aggregate(Max("price")) if review.space.detailspace_set.exists() else PRICE,
                "types"     : [types.name for types in review.space.types.all()]

            }
            for review in reviews
        ]
        return JsonResponse({"review_card":review_card}, status = 200)
