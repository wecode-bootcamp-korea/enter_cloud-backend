from django.views import View
from django.http import JsonResponse, HttpResponse
from .models import Reservation, Package, Time

class Reservation(View):
    def post(self, request, space_id):
        return JsonResponse({"message":"SUCCESS"}, status = 201)
