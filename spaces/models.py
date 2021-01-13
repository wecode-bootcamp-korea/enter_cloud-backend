from django.db import models

class Type(models.Model):
    name = models.CharField(max_length = 15)
    
    class Meta:
        db_table = "types"

class Space(models.Model):
    name                 = models.CharField(max_length = 18)
    simple_information   = models.CharField(max_length = 27)
    main_information     = models.CharField(max_length = 500)
    main_image           = models.URLField()
    site_url             = models.URLField(null = True)
    email                = models.EmailField()
    phone_number         = models.CharField(max_length = 11)
    main_phone_number    = models.CharField(max_length = 20)
    open_time            = models.IntegerField()
    close_time           = models.IntegerField()
    lat                  = models.DecimalField(max_digits = 10, decimal_places = 6, null = True)
    lng                  = models.DecimalField(max_digits = 10, decimal_places = 6, null = True)
    location             = models.CharField(max_length = 20, null = True)
    created_at           = models.DateTimeField(auto_now_add = True)
    updated_at           = models.DateTimeField(auto_now = True)
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
    image_url = models.URLField()
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
    image                = models.URLField()
    min_reservation_time = models.IntegerField()
    min_people           = models.IntegerField()
    max_people           = models.IntegerField()
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
    detail_space = models.ManyToManyField("DetailSpace", db_table = "detail_space_facilities")

    class Meta:
        db_table = "detail_facilities"


    