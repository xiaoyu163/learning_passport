from django.db import models
from users.models import Student
# Create your models here.

class Article (models.Model):
    date = models.DateField()
    type = models.CharField(max_length=20)
    title = models.CharField(max_length=50)
    platform = models.CharField(max_length=50, null=True)
    comp = models.CharField(max_length=100, null=True)
    award = models.CharField(max_length=50, null=True)
    status = models.BooleanField(null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    file = models.FileField(upload_to='article/', null=True)
    filename = models.CharField(max_length=100, null=True)
    published = models.BooleanField(null=True)
    apa = models.CharField(max_length=100, null=True)

