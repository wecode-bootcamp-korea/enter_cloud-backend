import json

from datetime           import datetime, timedelta
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
        try:
            data                = json.loads(request.body)
            reservation_day     = data["reservation_day"]
            reservation_people  = int(data["people"])
            name                = data["name"]
            phone_number        = data["phone_number"]
            email               = data.get("email")
            purpose             = data.get("purpose")
            reservation_request = data.get("reservation_request")
            package_id          = data.get("package_id")
            time_price_id       = data.get("time_id")
            user                = request.user
            detail_space        = DetailSpace.objects.get(id = detail_space_id)

            if package_id is not None:
                package             = PackagePrice.objects.get(id = package_id)
                start_time          = package.start_time
                end_time            = package.end_time
                allowed_people      = package.people
                excess_price        = package.excess_price
                except_excess_price = package.price

                if not package in detail_space.packageprice_set.all():
                    return JsonResponse({"message":"PACKAGE_NOT_IN_DETAIL_SPACE"}, status = 400)
            
            if time_price_id is not None:
                time_price          = TimePrice.objects.get(id = time_price_id)
                start_time          = data.get("start_time")
                end_time            = data.get("end_time")
                allowed_people      = time_price.people
                excess_price        = time_price.excess_price
                except_excess_price = time_price.price
            
                if not time_price in detail_space.timeprice_set.all():
                    return JsonResponse({"message":"TIME_PRICE_NOT_IN_DETAIL_SPACE"}, status = 400)
            
            start               = datetime.strptime(reservation_day + " " + start_time, "%Y-%m-%d %H")
            end                 = datetime.strptime(reservation_day + " " + end_time, "%Y-%m-%d %H")
            hours               = list(range(0, 24))

            if start_time > end_time : 
                end = end + timedelta(days = 1)
                
            if start < datetime.now():
                return JsonResponse({"message":"CAN_NOT_RESERVATION_BEFORE_TODAY"}, status = 400)

            if Reservation.objects.filter(start_time__gte = start, end_time__lte = end).exists():
                return JsonResponse({"message":"RESERVATION_ALREADY_EXIST"})

            if reservation_people > allowed_people:
                gap         = reservation_people - allowed_people
                add_price   = excess_price * gap

            reservation = Reservation.objects.create(
                user                 = user, 
                people               = reservation_people, 
                day                  = reservation_day, 
                start_time           = start, 
                end_time             = end, 
                detail_space         = detail_space
                )

            if package_id is not None:
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
        except ValueError:
            return JsonResponse({"meassage":"OUT_OF_RANGE_DAY"}, status = 400)
    

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
