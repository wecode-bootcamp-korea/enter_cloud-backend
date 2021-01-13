from django.db import models

from utils import TimeStampModel

class Review(TimeStampModel):
    content      = models.CharField(max_length = 300)
    space        = models.ForeignKey("spaces.Space", on_delete = models.CASCADE)
    user         = models.ForeignKey("users.User", on_delete = models.CASCADE)
    rating       = models.IntegerField()

    class Meta:
        db_table = "reviews"

class ReviewComment(TimeStampModel):
    content     = models.CharField(max_length = 300)
    host        = models.ForeignKey("users.Host", on_delete = models.CASCADE)
    review      = models.ForeignKey("Review", on_delete = models.CASCADE)
    
    class Meta:
        db_table = "review_comments"