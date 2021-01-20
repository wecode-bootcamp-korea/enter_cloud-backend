from django.db import models

from utils import TimeStampModel

class Type(models.Model):
    name = models.CharField(max_length = 15)
    
    class Meta:
        db_table = "types"

class Space(TimeStampModel):
    name                 = models.CharField(max_length = 18)
    simple_information   = models.CharField(max_length = 27)
    main_information     = models.CharField(max_length = 500)
    main_image           = models.URLField(max_length = 2000)
    site_url             = models.URLField(max_length = 2000, null = True)
    email                = models.EmailField(max_length = 245)
    phone_number         = models.CharField(max_length = 11)
    main_phone_number    = models.CharField(max_length = 20)
    open_time            = models.CharField(max_length = 10)
    close_time           = models.CharField(max_length = 10)
    latitude             = models.DecimalField(max_digits = 10, decimal_places = 6, null = True)
    longitude            = models.DecimalField(max_digits = 10, decimal_places = 6, null = True)
    location             = models.CharField(max_length = 20, null = True)
    host                 = models.ForeignKey("users.Host", on_delete = models.CASCADE)
    types                = models.ManyToManyField("Type", db_table = "space_types")

    class Meta:
        db_table = "spaces"

class SpaceTag(models.Model):
    space   = models.ForeignKey("Space", on_delete = models.CASCADE)
    tag     = models.ForeignKey("Tag", on_delete = models.CASCADE)

    class Meta:
        db_table = "space_tags"

class Tag(models.Model):
    name = models.CharField(max_length = 20)

    class Meta:
        db_table = "tags"

class SpaceFacility(models.Model):
    space    = models.ForeignKey("Space", on_delete = models.CASCADE)
    facility = models.ForeignKey("Facility", on_delete = models.CASCADE)

    class Meta:
        db_table = "space_facilities"

class Facility(models.Model):
    description = models.CharField(max_length = 100)
    
    class Meta:
        db_table = "facilities"

class SubImage(models.Model):
    image_url = models.URLField(max_length = 2000)
    space     = models.ForeignKey("Space", on_delete = models.CASCADE)

    class Meta:
        db_table = "sub_images"

class ReservationNote(models.Model):
    description = models.CharField(max_length = 100)
    space       = models.ForeignKey("Space", on_delete = models.CASCADE)

    class Meta:
        db_table = "reservation_notes"

class SpaceBreakday(models.Model):
    space    = models.ForeignKey("Space", on_delete = models.CASCADE)
    breakday = models.ForeignKey("Breakday", on_delete = models.CASCADE)

    class Meta:
        db_table = "space_breakdays"

class BreakDay(models.Model):
    day = models.CharField(max_length = 10)

    class Meta:
        db_table = "breakdays"

class DetailSpace(models.Model):
    name                 = models.CharField(max_length = 18)
    information          = models.CharField(max_length = 500)
    image                = models.URLField(max_length = 2000)
    min_reservation_time = models.IntegerField()
    min_people           = models.IntegerField()
    max_people           = models.IntegerField()
    price                = models.IntegerField()
    space                = models.ForeignKey("Space", on_delete = models.CASCADE)

    class Meta:
        db_table = "detail_spaces"

class DetailType(models.Model):
    detail_space = models.ManyToManyField("DetailSpace", db_table = "detail_space_types")
    name         = models.CharField(max_length = 45)
    
    class Meta:
        db_table = "detail_types"

class DetailFacility(models.Model):
    name         = models.CharField(max_length = 45)
    english_name = models.CharField(max_length = 45)
    detail_space = models.ManyToManyField("DetailSpace", db_table = "detail_space_facilities")

    class Meta:
        db_table = "detail_facilities"

class PackagePrice(TimeStampModel):
    name = models.CharField(max_length = 18)
    start_time = models.IntegerField()
    end_time = models.IntegerField()
    price = models.IntegerField()
    people = models.IntegerField()
    excess_price = models.IntegerField()
    detail_space = models.ForeignKey("spaces.DetailSpace", on_delete = models.CASCADE)

    class Meta:
        db_table = "package_prices"
    
class TimePrice(TimeStampModel):
    time_reservation_type = models.CharField(max_length = 20)
    excess_price = models.IntegerField(null = True)
    price = models.IntegerField()
    detail_space = models.ForeignKey("DetailSpace", on_delete = models.CASCADE)

    class Meta:
        db_table = "time_prices"
class Like(models.Model):
    user     = models.ForeignKey("users.User", on_delete = models.CASCADE)
    space    = models.ForeignKey("spaces.Space", on_delete = models.CASCADE)
    is_liked = models.BooleanField(default = False)

    class Meta:
        db_table = "likes"
    
