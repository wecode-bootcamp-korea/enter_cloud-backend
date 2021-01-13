from django.db import models

class User(models.Model):
    nickname     = models.CharField(max_length = 20, unique = True)
    email        = models.EmailField(max_length = 245, unique = True)
    password     = models.CharField(max_length = 100)
    phone_number = models.CharField(max_length= 11, null = True)
    avatar_image = models.URLField(max_length = 2000, null = True)

    class Meta:
        db_table = "users"

class Host(models.Model):
    user                = models.OneToOneField("User", on_delete = models.CASCADE)
    host_avatar_image   = models.URLField(max_length = 2000, null = True)
    
    class Meta:
        db_table = "hosts"

