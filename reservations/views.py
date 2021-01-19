import json
from dateutil.parser import parse
from datetime import datetime
from django.views import View
from django.http  import JsonResponse

from .models import Reservation, ReservationInformation
from spaces.models import PackagePrice, TimePrice, DetailSpace
from decorators.utils import login_required

class ReservationView(View):
    @login_required
    def post(self, request, space_id):
        data                = json.loads(request.body)
        reservation_day     = data["day"]
        package_id          = data["package_id"]
        name                = data["name"]
        phone_number        = data["phone_number"]
        reservation_type    = data["reservation_type"]
        email               = data.get("email")
        purpose             = data.get("purpose")
        reservation_request = data.get("reservation_request")
        start_time          = int(data["start_time"])
        end_time            = int(data["end_time"])
        year, month, day    = reservation_day.split("-")
        start               = datetime(int(year), int(month), int(day), start_time)
        end                 = datetime(int(year), int(month), int(day), end_time)
        package             = PackagePrice.objects.get(id = package_id)
        user                = request.user
        detail_space        = DetailSpace.objects.get(id = data["detail_space_id"])

        if start > end:
            return JsonResponse({"message":"WRONG_TIME"}, status = 400)
        
        if Reservation.objects.filter(day = reservation_day, start_time__gte = start, end_time__lte = end).exists():
            return JsonResponse({"message":"ALREADY_EXIST"}, status = 400)
    
        reservation = Reservation.objects.create(
            reservation_type = reservation_type,
            people = 4, 
            day = reservation_day, 
            start_time = start,
            end_time = end,
            user = user, 
            package = package
            )

        ReservationInformation.objects.create(
            reservation = reservation, 
            name = name, 
            phone_number = phone_number, 
            email = email, 
            purpose = purpose, 
            reservation_request = reservation_request
            )
    
        return JsonResponse({"message":"SUCCESS"}, status = 201)

    def get(self, request, space_id):
        
        return JsonResponse({"message":"SUCCESS"}, status = 200)
