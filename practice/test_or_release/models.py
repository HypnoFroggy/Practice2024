from django.db import models


class Vacancy(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    department = models.TextField()
    has_test = models.BooleanField()
    response_letter_required = models.BooleanField()
    area = models.TextField(default='')
    salary = models.TextField()
    description = models.TextField()
    experience = models.TextField(default='')
    is_open = models.BooleanField()
    address = models.TextField()
    url = models.URLField()
    employer = models.URLField()

