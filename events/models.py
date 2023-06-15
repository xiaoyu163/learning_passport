from django.db import models
from users.models import Student, User, Organisation
# Create your models here.
class Events(models.Model):
    c_name = models.CharField(unique=True, max_length=50)
    e_name = models.CharField(unique=True, max_length=50)
    TYPE = (
        (1, 'Seminar'),
        (2, 'Conference'),
        (3, 'Proposal Defense'),
        (4, 'Candidatual Defense'),
        (5, 'Freshman Month / Week'),
        (6, 'The Night of Chinese Studies Department'),
        (7, 'Creative Writing'),
        (8, 'Others'),               
    )  
    type = models.SmallIntegerField(choices=TYPE)
    start = models.DateTimeField()
    end = models.DateTimeField()
    venue = models.CharField(max_length=100)
    desc = models.CharField(max_length=200)
    internal = models.BooleanField()
    speaker = models.CharField(max_length=50)    
    attendance = models.BooleanField()
    file = models.FileField(upload_to="event_com/")


class Event_Participants(models.Model):
    event = models.ForeignKey(Events, on_delete=models.PROTECT, null=True)
    student = models.ForeignKey(Student, on_delete=models.PROTECT, null=True)
    position = models.CharField(max_length=50)
    attendance = models.BooleanField(null=True, default=0)
    registered = models.BooleanField(null=True)

class Comittee(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT, null=True)
    event = models.ForeignKey(Events, on_delete=models.PROTECT, null=True)
    organisation = models.ForeignKey(Organisation, on_delete=models.PROTECT, null=True)
    position = models.CharField(max_length=50)
    award = models.CharField(max_length=50)
class OtherComp (models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT, null=True)
    year = models.IntegerField()
    name = models.CharField(max_length=100)
    award = models.CharField(max_length=50)

class Announcement (models.Model):
    content = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    TYPE = (
        ("General", "General"),
        ("Event", "Event"),
        ("Others", "Others"),
    )
    category = models.CharField(max_length=10,choices=TYPE)
    display_to = models.CharField(max_length=100)
    created_time = models.DateTimeField(auto_now=True)