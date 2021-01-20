import json

from datetime           import datetime
from django.views       import View
from django.http        import JsonResponse
from django.db.models   import Q

from .models            import Reservation, ReservationInformation
from spaces.models      import Space, DetailSpace
from spaces.models      import PackagePrice, TimePrice, DetailSpace
from decorators.utils   import login_required

class ReservationView(View):
    @login_required
    def post(self, request, detail_space_id):
        data                = json.loads(request.body)
        reservation_type    = data["reservation_type"]
        reservation_day     = data["day"]
        reservation_people  = int(data["people"])
        name                = data["name"]
        phone_number        = data["phone_number"]
        email               = data.get("email")
        purpose             = data.get("purpose")
        reservation_request = data.get("reservation_request")
        user                = request.user
        detail_space        = DetailSpace.objects.get(id = detail_space_id)

        if reservation_type == "패키지":
            package_id          = data["package_id"]
            package             = PackagePrice.objects.get(id = package_id)
            start_time          = package.start_time
            end_time            = package.end_time
            allowed_people      = package.people
            excess_price        = package.excess_price
            except_excess_price = package.price

            if not package in detail_space.packageprice_set.all():
                return JsonResponse({"message":"PACKAGE_NOT_IN_DETAIL_SPACE"}, status = 400)
        
        if reservation_type == "시간":
            time_price_id       = data["time_id"]
            time_price          = TimePrice.objects.get(id = time_price_id)
            start_time          = int(data.get("start_time"))
            end_time            = int(data.get("end_time"))
            allowed_people      = time_price.people
            excess_price        = time_price.excess_price
            except_excess_price = time_price.price
           
            if not time_price in detail_space.timeprice_set.all():
                return JsonResponse({"message":"TIME_PRICE_NOT_IN_DETAIL_SPACE"}, status = 400)
        
        year, month, day    = reservation_day.split("-")
        start               = datetime(int(year), int(month), int(day), start_time)
        end                 = datetime(int(year), int(month), int(day), end_time)

        if reservation_people > allowed_people:
            gap         = reservation_people - allowed_people
            add_price   = excess_price * gap
            
        if start > end:
            return JsonResponse({"message":"WRONG_TIME"}, status = 400) 
        
        day_check   = Reservation.objects.filter(day = reservation_day)
        hours       = list(range(0, 24))

        for check in day_check:
            for hour in range(check.start_time.hour, check.end_time.hour):
                hours.remove(hour)

        for reservation_time in range(start_time, end_time+1):
            if not  reservation_time in hours:
                return JsonResponse({"message":"CAN_NOT_RESERVATION"}, status = 400)

        reservation = Reservation.objects.create(
            user                 = user, 
            reservation_type     = reservation_type, 
            people               = reservation_people, 
            day                  = reservation_day, 
            start_time           = start, 
            end_time             = end, 
            detail_space         = detail_space
            )

        if reservation_type == "패키지":
            reservation.package = package
        else:
            reservation.time = time_price
        reservation.save()

        ReservationInformation.objects.create(
            reservation          = reservation, 
            name                 = name, 
            phone_number         = phone_number, 
            email                = email, 
            purpose              = purpose, 
            reservation_request  = reservation_request,
            price                = except_excess_price + add_price
            )
        return JsonResponse({"message":"SUCCESS"}, status = 201)

    def get(self, request, detail_space_id):
        data             = json.loads(request.body)
        detail_space     = DetailSpace.objects.get(id = detail_space_id)
        reservation_list = detail_space.reservation_set.all()
        reservation_data = [
            {
                "day"           :reservation.day,
                "start_time"    :reservation.start_time,
                "end_time"      :reservation.end_time
            }
            for reservation in reservation_list
        ]
        return JsonResponse({"reservation_data":reservation_data}, status = 200)
