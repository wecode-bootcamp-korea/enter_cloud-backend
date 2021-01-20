import json
import math

from django.views       import View
from django.http        import JsonResponse
from django.db.models   import Max
from django.db import connection

from spaces.models      import Space, Like, Type
from users.models       import Host  
from reviews.models     import Review
from reviews.views      import ReviewView
from decorators.utils   import login_required

PRICE = 5000
MAX_PEOPLE = 10

class SpaceCardView(View):
    def get(self, request):
        try:
            PAGE_SIZE    = 9
            space_type   = request.GET.get("type", "카페")
            location     = request.GET.get("location")
            page         = int(request.GET.get("page", 1))
            limit        = page * PAGE_SIZE
            offset       = limit - PAGE_SIZE
            search_type  = Type.objects.get(name = space_type)
            spaces       = Space.objects.all().order_by("?").\
                            select_related("host").\
                            prefetch_related("host__user", "spacetag_set", "subimage_set", "detailspace_set", "spacetag_set__tag").\
                            filter(types__in = [search_type])    

            if location is not None:
                spaces = spaces.filter(location__icontains = location)
            
            space_card = [
                {
                    "id"            : space.id,
                    "name"          : space.name,
                    "host"          : space.host.user.nickname,
                    "location"      : space.location,
                    "count_review"  : space.review_set.count(),
                    "main_image"    : space.main_image,
                    "max_people"    : space.detailspace_set.aggregate(Max("max_people"))["max_people__max"] if space.detailspace_set.exists() else MAX_PEOPLE,
                    "price"         : space.detailspace_set.aggregate(Max("price"))["price__max"] if space.detailspace_set.exists() else PRICE,
                    "tags"          : [tag.tag.name for tag in space.spacetag_set.all()],
                    "tags"          : [space_type.name for space_type in space.types.all()],
                    "sub_image"     : [sub_image.image_url for sub_image in space.subimage_set.all()],
                }
                for space in spaces[offset:limit]
                ]
            return JsonResponse({"space_card":space_card}, status = 200)
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status = 400)

class SpaceDetailView(View):
    def get(self, request, space_id):
        try:
            space = Space.objects.get(id = space_id)
            main_space = [
                {
                    "id"                        : space.id,
                    "name"                      : space.name,
                    "simple_information"        : space.simple_information,
                    "main_image"                : space.main_image,
                    "tags"                      : [space.tag.name for space in space.spacetag_set.all()],
                    "main_information"          : space.main_information,
                    "open_time"                 : space.open_time,
                    "close_time"                : space.close_time,
                    "site_url"                  : space.site_url,
                    "sub_images"                : [sub_image.image_url for sub_image in space.subimage_set.all()],
                    "break_days"                : [breakday.breakday.day for breakday in space.spacebreakday_set.all()],
                    "facilities_informations"   : [facility.facility.description for facility in space.spacefacility_set.all()],
                    "reservation_notes"         : [note.description for note in space.reservationnote_set.all()],
                }
            ]

            detail_space = [
                {
                    "id"                    : detail_space.id,
                    "name"                  : detail_space.name,
                    "price"                 : detail_space.price,
                    "image"                 : detail_space.image,
                    "information"           : detail_space.information,
                    "types"                 : [detail_space_type.name for detail_space_type in detail_space.detailtype_set.all()],
                    "min_reservation_time"  : detail_space.min_reservation_time,
                    "min_people"            : detail_space.min_people,
                    "max_people"            : detail_space.max_people,
                    "facilities"            : [
                        {
                            "name": facility.name,
                            "type": facility.english_name
                        }
                        for facility in detail_space.detailfacility_set.all()
                    ],
                }
                for detail_space in space.detailspace_set.all().prefetch_related("detailfacility_set", "detailtype_set")
            ]

            return JsonResponse({"main":main_space, "detail":detail_space}, status = 200)
        except Space.DoesNotExist:
            return JsonResponse({"message":"SPACE_DOES_NOT_EXIST"}, status = 400)

class LikeView(View):
    @login_required
    def patch(self, request, space_id):
        try:
            space    = Space.objects.get(id = space_id)
            user     = request.user
            
            if Like.objects.filter(user = user, space = space).exists():
                like = Like.objects.get(user = user, space = space)
                if like.is_liked == True:
                    like.is_liked = False
                    like.save()
                    return JsonResponse({"message":"UNLIKE"}, status = 200)
                like.is_liked = True
                like.save()
                return JsonResponse({"message":"LIKE"}, status = 200)
            Like.objects.create(user = user, space = space, is_liked = True)
            return JsonResponse({"message":"LIKE"}, status = 201)
        except Space.DoesNotExist:
            return JsonResponse({"message":"SPACE_DOES_NOT_EXIST"}, status = 400)