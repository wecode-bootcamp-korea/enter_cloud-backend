import json
from django.http import JsonResponse, HttpResponse

from django.views   import View
from spaces.models  import DetailSpace
from .models        import Reservation, Package, Time

class ReservationView(View):
    def post(self, request, space_id):
        data = json.loads(request.body)
        reservation_type = data["reservation_type"]
        time = data.get("time")
        start_time = data["start_time"]
        end_time = data["end_time"]
        people = data["people"]
        detail_space = DetailSpace.objects.get(id = data["detail_space_id"])
        user = request.user
 
        
        return JsonResponse({"message":"SUCCESS"}, status = 201)
