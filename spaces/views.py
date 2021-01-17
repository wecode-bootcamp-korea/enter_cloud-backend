import json

from django.views       import View
from django.http        import JsonResponse, HttpResponse
from django.db.models   import Max

from spaces.models      import Space, Like
from users.models       import Host  
from reviews.models     import Review
from decorators.utils   import login_required

class SpaceCardView(View):
    def get(self, request):
        spaces = Space.objects.all().order_by("?").select_related("host").prefetch_related("review_set", "spacetag_set", "subimage_set", 
                                                                                            "detailspace_set", "host__user", "spacetag_set__tag")
        data = [
            {
                "name"          : space.name,
                "host"          : space.host.user.nickname,
                "location"      : space.location,
                "count_review"  : space.review_set.count(),
                "main_image"    : space.main_image.strip('\,\n\"'),
                "max_people"    : space.detailspace_set.aggregate(Max("max_people")) if space.detailspace_set.exists() else 10,
                "price"         : space.detailspace_set.annotate(Max("price"))[0].price if space.detailspace_set.exists() else 5000,
                "tags":[
                    {
                        "tag" : tag.tag.name
                    }
                    for tag in space.spacetag_set.all()
                ],
                "sub_image":[
                    {
                        "sub_image": sub_image.image_url.strip('\,\n\"'),
                    }
                    for sub_image in space.subimage_set.all()
                ],
            }
            for space in spaces
            ]
        self.space_card = data
        return JsonResponse({"data":data}, status = 200)

class SpaceView(SpaceCardView):
    def get(self, request):
        super().get(request)
        reviews = Review.objects.all().order_by("-created_at").select_related("space").prefetch_related("space__detailspace_set", 
                                                                                                        "space__spacetag_set__tag")
        review_card = [
            {
                "name"      : review.space.name,
                "content"   : review.content,
                "rating"    : review.rating,
                "price"     : review.space.detailspace_set.all().aggregate(Max("price")) if review.space.detailspace_set.exists() else 5000,
                "tags":[
                    {
                        "tag":tag.tag.name
                    }
                    for tag in review.space.spacetag_set.all()
                ]
            }
            for review in reviews
        ]
        return JsonResponse({"space_card":self.space_card, "review_card":review_card}, status = 200)

class LikeView(View):
    @login_required
    def post(self, request, space_id):
        try:
            space    = Space.objects.get(id = space_id)
            user     = request.user
            like     = Like.objects.filter(user = user, space = space)
            if not like.exists():
                like.create(user = user, space = space)
                return HttpResponse("LIKE")
            return HttpResponse("HTTP_METHOD_WRONG")
        except Space.DoesNotExist:
            return HttpResponse("SPACE_DOES_NOT_EXIST")
        except KeyError:
            return HttpResponse("KEY_ERROR")
    
    @login_required
    def delete(self, request, space_id):
        try:
            space    = Space.objects.get(id = space_id)
            user     = request.user
            like     = Like.objects.filter(user = user, space = space)
            if like.exists():
                like.delete()
                return HttpResponse("UNLIKE")
            return HttpResponse("HTTP_METHOD_WRONG")
        except Space.DoesNotExist:
            return HttpResponse("SPACE_DOES_NOT_EXIST")
        except KeyError:
            return HttpResponse("KEY_ERROR")

