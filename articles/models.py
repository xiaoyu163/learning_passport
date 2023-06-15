from django.db import models
from users.models import Student
# Create your models here.

class Article (models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    year = models.IntegerField()
    type = models.CharField(max_length=20)
    title = models.CharField(max_length=50)
    platform = models.CharField(max_length=50, null=True)
    comp = models.CharField(max_length=100, null=True)
    award = models.CharField(max_length=50, null=True)
    submission = models.FileField()
    status = models.BooleanField()
    file = models.FileField(upload_to='article/')
