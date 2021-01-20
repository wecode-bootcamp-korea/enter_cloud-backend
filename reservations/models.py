from django.db import models
from django.utils import timezone

from utils import TimeStampModel

class Reservation(models.Model):
    reservation_type = models.CharField(max_length = 20)
    people = models.IntegerField()
    day = models.DateField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length = 20, default = "pending")
    user = models.ForeignKey("users.User", on_delete = models.CASCADE)
    package = models.ForeignKey("spaces.PackagePrice", on_delete = models.CASCADE, null = True)
    time = models.ForeignKey("spaces.TimePrice", on_delete = models.CASCADE, null = True)
    detail_space = models.ForeignKey("spaces.DetailSpace", on_delete = models.CASCADE)

    class Meta:
        db_table = "reservations"

class ReservationInformation(models.Model):
    reservation = models.OneToOneField("Reservation", on_delete = models.CASCADE)
    name = models.CharField(max_length = 45)
    phone_number = models.CharField(max_length = 11)
    email = models.EmailField(max_length = 245, null = True)
    purpose = models.CharField(max_length = 30, null = True)
    price = models.IntegerField()
    reservation_request = models.CharField(max_length = 500, null = True)

    class Meta:
        db_table = "reservation_informations"