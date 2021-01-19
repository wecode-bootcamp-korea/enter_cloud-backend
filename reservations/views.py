from django.views import View
from django.http  import JsonResponse

from .models import Reservation

class ReservationView(View):
    def post(self, request, space_id):
        
        return JsonResponse({"message":"SDF"}, status = 200)
