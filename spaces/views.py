import json
import random
import math

from django.views       import View
from django.http        import JsonResponse
from django.db.models   import Max

from spaces.models      import Space, Like, Type
from users.models       import Host  
from reviews.models     import Review
from reviews.views      import ReviewView
from decorators.utils   import login_required

PRICE = 5000
MAX_PEOPLE = 10

class SpaceCardView(View):
    def get(self, request):
        spaces      = Space.objects.all().order_by("?").select_related("host").prefetch_related("host__user", "spacetag_set", "subimage_set", 
                                                                                            "detailspace_set", "spacetag_set__tag")
        space_card = [
            {
                "id"            : space.id,
                "name"          : space.name,
                "host"          : space.host.user.nickname,
                "location"      : space.location,
                "count_review"  : space.review_set.count(),
                "main_image"    : space.main_image.strip('\,\n\"'),
                "max_people"    : space.detailspace_set.aggregate(Max("max_people"))["max_people__max"] if space.detailspace_set.exists() else MAX_PEOPLE,
                "price"         : space.detailspace_set.aggregate(Max("price"))["price__max"] if space.detailspace_set.exists() else PRICE,
                "tags"          : [tag.tag.name for tag in space.spacetag_set.all()],
                "sub_image"     : [sub_image.image_url.strip('\,\n\"') for sub_image in space.subimage_set.all()],
            }
            for space in spaces[0:9]
            ]
        return JsonResponse({"space_card":space_card}, status = 200)

class SpaceDetailView(View):
    def get(self, request, space_id):
        try:
            space = Space.objects.get(id = space_id)
            main_space = [
                {
                    "id"                        : space.id,
                    "name"                      : space.name,
                    "simple_information"        : space.simple_information,
                    "main_image"                : space.main_image.strip('\,\n\"'),
                    "tags"                      : [space.tag.name for space in space.spacetag_set.all()],
                    "main_information"          : space.main_information,
                    "open_time"                 : space.open_time,
                    "close_time"                : space.close_time,
                    "site_url"                  : space.site_url,
                    "sub_images"                : [sub_image.image_url.strip('\,\n\"') for sub_image in space.subimage_set.all()],
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
                    "image"                 : detail_space.image.strip('\,\n\"'),
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

class SpaceListView(View):
    def get(self, request):
        try:
            search_list     = list(request.GET.get("q").split())
            search_type     = search_list[0]

            if len(search_list) == 2:
                search_location = search_list[1]
            else:
                search_location = None

            if Type.objects.filter(name = search_type).exists():
                space_type = Type.objects.get(name = search_type)
            else:
                space_type = Type.objects.get(name = "카페")
            
            spaces = space_type.space_set.all().select_related("host")\
                .prefetch_related("detailspace_set", "subimage_set", "spacetag_set__tag", "host__user", "review_set")

            if search_location:
                spaces = spaces.filter(location__icontains = search_location)        

            PAGE_SIZE       = 9
            page            = int(request.GET.get("page", 1))
            max_page        = math.ceil(len(spaces) / PAGE_SIZE)

            if page > max_page or page < 1:
                page = 1
        
            limit           = int(page) * PAGE_SIZE
            offset          = limit - PAGE_SIZE
            space_cards = [
                {
                    "id"            : space.id,
                    "name"          : space.name,
                    "host"          : space.host.user.nickname,
                    "location"      : space.location,
                    "count_review"  : space.review_set.count(),
                    "main_image"    : space.main_image.strip('\,\n\"'),
                    "max_people"    : space.detailspace_set.aggregate(Max("max_people"))["max_people__max"]
                                    if space.detailspace_set.exists()
                                    else MAX_PEOPLE,
                    "price"         : space.detailspace_set.annotate(space_price = Max("price"))[0].price 
                                    if space.detailspace_set.exists() 
                                    else PRICE,
                    "tags"          : [tag.tag.name for tag in space.spacetag_set.all()],
                    "sub_image"     : [sub_image.image_url.strip('\,\n\"') for sub_image in space.subimage_set.all()],
                }
                for space in spaces[offset:limit]
                ]

            return JsonResponse({"space_cards":space_cards}, status = 200)
        except AttributeError:
            return JsonResponse({"message":"SEARCH_WORD_REQUIRED"}, status = 400)

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