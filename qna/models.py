from django.db import models
from utils import TimeStampModel

class Question(TimeStampModel):
    content      = models.CharField(max_length = 300)
    user         = models.ForeignKey("users.User", on_delete = models.CASCADE)
    space        = models.ForeignKey("spaces.Space", on_delete = models.CASCADE)

    class Meta:
        db_table = "questions"

class Answer(TimeStampModel):
    content      = models.CharField(max_length = 300)
    host         = models.ForeignKey("users.Host", on_delete = models.CASCADE)
    question     = models.ForeignKey("Question", on_delete = models.CASCADE)

    class Meta:
        db_table = "answers"
    