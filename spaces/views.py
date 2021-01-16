import json
import random

from django.views       import View
from django.http        import JsonResponse, HttpResponse
from django.db.models   import Max
from django.db          import connection

from spaces.models      import Space
from users.models       import Host  
from reviews.models     import Review


class SpaceCardView(View):
    def get(self, request):
        spaces = Space.objects.all().order_by("?").select_related("host").prefetch_related("review_set", "spacetag_set", "subimage_set", 
                                                                                            "detailspace_set", "host__user", "spacetag_set__tag")
        print(request.GET.get("q"))
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
                "tags"      : [tag.tag.name for tag in review.space.spacetag_set.all()]
            }
            for review in reviews
        ]
        return JsonResponse({"space_card":self.space_card, "review_card":review_card}, status = 200)

class SpaceDetailView(View):
    def get(self, request, space_id):
        try:
            space = Space.objects.get(id = space_id)
            
            main_space = [
                {
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
                    "name"                  : detail_space.name,
                    "price"                 : detail_space.price,
                    "image"                 : detail_space.image.strip('\,\n\"'),
                    "information"           : detail_space.information,
                    "types"                 : [detail_space_type.name for detail_space_type in detail_space.detailtype_set.all()],
                    "min_reservation_time"  : detail_space.min_reservation_time,
                    "min_people"            : detail_space.min_people,
                    "max_poeple"            : detail_space.max_people,
                    "facilities"            : [facility.name for facility in detail_space.detailfacility_set.all()],
                }
                for detail_space in space.detailspace_set.all().prefetch_related("detailfacility_set", "detailtype_set")
            ]

            return JsonResponse({"main":main_space, "detail":detail_space}, status = 200)
        except Space.DoesNotExist:
            return HttpResponse("SPACE_DOES_NOT_EXIST", status = 400)