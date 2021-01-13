from django.db import models

class Question(models.Model):
    content      = models.CharField(max_length = 300)
    user         = models.ForeignKey("users.User", on_delete = models.CASCADE)
    space        = models.ForeignKey("spaces.Space", on_delete = models.CASCADE)
    created_at   = models.DateTimeField(auto_now_add = True)
    updated_at   = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = "questions"

class Answer(models.Model):
    content      = models.CharField(max_length = 300)
    host         = models.ForeignKey("users.Host", on_delete = models.CASCADE)
    question     = models.ForeignKey("Question", on_delete = models.CASCADE)
    created_at   = models.DateTimeField(auto_now_add = True)
    updated_at   = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = "answers"
    