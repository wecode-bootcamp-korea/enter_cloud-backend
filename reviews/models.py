from django.db import models

class Review(models.Model):
    content      = models.CharField(max_length = 300)
    space        = models.ForeignKey("spaces.Space", on_delete = models.CASCADE)
    user         = models.ForeignKey("users.User", on_delete = models.CASCADE)
    rating       = models.IntegerField()
    created_at   = models.DateTimeField(auto_now_add = True)
    updated_at   = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = "reviews"

class ReviewComment(models.Model):
    content     = models.CharField(max_length = 300)
    host        = models.ForeignKey("users.Host", on_delete = models.CASCADE)
    review      = models.ForeignKey("Review", on_delete = models.CASCADE)
    created_at  = models.DateTimeField(auto_now_add = True)
    updated_at  = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = "review_comments"