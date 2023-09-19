from django.db import models
from users.models import Student, User, Organisation
# Create your models here.
class Events(models.Model):
    c_name = models.CharField(max_length=50)
    e_name = models.CharField(max_length=50)
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
    year = models.IntegerField()
    venue = models.CharField(max_length=100)
    desc = models.CharField(max_length=200)
    internal = models.BooleanField()
    speaker = models.CharField(max_length=50)    
    attendance = models.BooleanField()
    poster = models.FileField(upload_to='event_poster/')
    file = models.FileField(upload_to='event_com/')
    file_by = models.ForeignKey(Student, on_delete=models.PROTECT, null=True)
    status = models.BooleanField(null=True)

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
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
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