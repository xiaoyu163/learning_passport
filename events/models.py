from django.db import models
from users.models import Student, User, Organisation
# Create your models here.
class Events(models.Model):
    c_name = models.CharField(max_length=50, null=True)
    e_name = models.CharField(max_length=50)
    TYPE = (
        (1, 'Seminar/Talk'),
        (2, 'Conference'),
        (3, 'Proposal Defense'),
        (4, 'Candidatual Defense'),
        (5, 'Welcome Week/Month'),
        (6, 'Chinese Studies Night'),
        (7, 'Workshop'),
        (8, 'Others'),               
    )  
    type = models.SmallIntegerField(choices=TYPE, null=True)
    start = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)
    year = models.IntegerField()
    venue = models.CharField(max_length=100, null=True)
    desc = models.CharField(max_length=200, null=True)
    internal = models.BooleanField()
    speaker = models.CharField(max_length=50, null=True)    
    attendance = models.BooleanField(null=True)
    enable_attendance = models.BooleanField(null=True)
    file = models.FileField(upload_to='event_com/', null=True)
    filename = models.CharField(max_length=100, null=True)
    file_by = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    status = models.BooleanField(null=True)
    poster = models.FileField(upload_to='event_poster/', null=True)


class Event_Participants(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    position = models.CharField(max_length=50, null=True)
    attendance = models.BooleanField(null=True, default=0)
    registered = models.BooleanField(null=True)
    file = models.FileField(upload_to='event_external/', null=True)
    filename = models.CharField(max_length=100, null=True)
    status = models.BooleanField(null=True)

class OtherComp (models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    year = models.IntegerField()
    name = models.CharField(max_length=100)
    award = models.CharField(max_length=50)
    status = models.BooleanField(null=True)
    file = models.FileField(upload_to='event_other/', null=True)
    filename = models.CharField(max_length=100, null=True)

class Announcement (models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    TYPE = (
        (1, "General"),
        (2, "Event"),
        (3, "Others"),
    )
    category = models.SmallIntegerField(choices=TYPE)
    LEVEL = (
        (1, "All"),
        (2, "Undergrad"),
        (3, "Postgrad"),
    )
    display_to = models.SmallIntegerField(choices=LEVEL)
    created_time = models.DateTimeField(auto_now=True)