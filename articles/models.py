from django.db import models
from users.models import Student
# Create your models here.

class Article (models.Model):

    year = models.IntegerField()
    type = models.CharField(max_length=20)
    title = models.CharField(max_length=50)
    platform = models.CharField(max_length=50, null=True)
    comp = models.CharField(max_length=100, null=True)
    award = models.CharField(max_length=50, null=True)
    status = models.BooleanField(null=True)
    file_by = models.ForeignKey(Student, on_delete=models.PROTECT)
    file = models.FileField(upload_to='article/')
