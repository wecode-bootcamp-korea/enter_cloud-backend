import json
import math

from django.views       import View
from django.http        import JsonResponse
from django.db.models   import Max

from spaces.models      import Space
from users.models       import Host  
from reviews.models     import Review

class SpaceCardView(View):
    def get(self, request):
        spaces       = Space.objects.all().order_by("?").select_related("host").prefetch_related("types", "review_set", "spacetag_set", "subimage_set", 
                                                                                            "detailspace_set", "host__user", "spacetag_set__tag")
        data = [
            {
                "name"          : space.name,
                "host"          : space.host.user.nickname,
                "location"      : space.location,
                "count_review"  : space.review_set.count(),
                "main_image"    : space.main_image.strip('\,\n\"'),
                "max_people"    : space.detailspace_set.aggregate(Max("max_people"))["max_people__max"] if space.detailspace_set.exists() else 10,
                "price"         : space.detailspace_set.aggregate(Max("price"))["price__max"] if space.detailspace_set.exists() else 5000,
                "tags"          : [tag.tag.name for tag in space.spacetag_set.all()],
                "sub_image"     : [sub_image.image_url.strip('\,\n\"') for sub_image in space.subimage_set.all()],
                "types"         : [space_type.name for space_type in space.types.all()]
            }
            for space in spaces
            ]

        self.space_card = data
        return JsonResponse({"data":data}, status = 200)

class SpaceView(SpaceCardView):
    def get(self, request):
        super().get(request)
        space_count = len(self.space_card)
        reviews     = Review.objects.all().order_by("-created_at").select_related("space").prefetch_related("space__detailspace_set", 
                                                                                                        "space__spacetag_set__tag")
        review_card = [
            {
                "name"      : review.space.name,
                "content"   : review.content,
                "rating"    : review.rating,
                "price"     : review.space.detailspace_set.all().aggregate(Max("price"))["price__max"] if review.space.detailspace_set.exists() else 5000,
                "tags"      : [tag.tag.name for tag in review.space.spacetag_set.all()]
            }
            for review in reviews
        ]
        if space_count < 10 :
            return JsonResponse({"space_card":self.space_card, "review_card":review_card}, status = 200)
        return JsonResponse({"space_card":self.space_card[:9], "review_card":review_card}, status = 200)

class SpaceListView(SpaceCardView):
    def get(self, request):
        super().get(request)
        PAGE_SIZE    = 6
        word         = request.GET.get("type")
        request_page = request.GET.get("page")
        get_page     = lambda x : 1 if request_page is None else request_page
        page         = int(get_page(request_page))
        limit        = page * PAGE_SIZE
        offset       = limit - PAGE_SIZE
        space_count  = len(self.space_card)
        max_page     = math.ceil(space_count / PAGE_SIZE)
        search_card  = []

        for card in self.space_card:
            space_type_list = card.get("types")
            if word in space_type_list:
                search_card.append(card)      

        if page < 1 or page > max_page:
            return JsonResponse({"space_card":search_card[0:PAGE_SIZE]})
            
        return JsonResponse({"space_card":search_card[offset:limit]}, status = 200)     
        