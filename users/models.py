from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users require an email field')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
    
class User(AbstractUser):
    objects = UserManager()
    email = models.EmailField('email adress', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    first_name = None
    last_name = None
    username = None
    full_name = models.CharField(max_length=50)
    name_chi = models.CharField(max_length=50, null=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(auto_now=True)
    ROLES = (
        ("SUPER ADMIN", "SUPER ADMIN"),
        ("ADMIN", "ADMIN"),
        ("HEAD OF DEPARTMENT", "HEAD OF DEPARTMENT"),
        ("LECTURER", "LECTURER"),
        ("STUDENT", "STUDENT"),
    )  
    role = models.CharField(max_length=20, choices=ROLES, default="STUDENT")
    is_active = models.BooleanField(default=True)
    contact = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=100, null=True)
    date_inactive = models.DateField(null=True)




class Semester (models.Model):
    academic_year = models.CharField(max_length=7)
    semester = models.SmallIntegerField()
    start = models.DateField()
    end = models.DateField()
    
class Lecturer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Position = (
        (1, "Adjunct Professor"),
        (2, "Associate Professor"),
        (3, "Senior Lecturer"),
        (4, "Lecturer"),
        (5, "Post Doctoral Research Fellow"),       
    )
    position = models.SmallIntegerField(choices=Position)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    matric_no = models.CharField(max_length=10)
    enrol_year = models.DateField(null=True)
    grad_year = models.DateField(null=True)
    Program = (
        (1, "Bachelor of Arts Chinese Studies"),
        (2, "Master of Chinese Studies (Coursework)"),
        (3, "Master of Arts (Research)"),
        (4, "Doctor of Philosophy (Ph.D)"),
    )
    program = models.SmallIntegerField(choices=Program)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.PROTECT)

class Organisation(models.Model):
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    internal = models.BooleanField()
    file = models.FileField(upload_to='org_com/')
    filename = models.CharField(max_length=100, null = True)
    file_by = models.ForeignKey(Student, on_delete=models.PROTECT, null=True)
    status = models.BooleanField(null=True)

class OrgComittee(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    org = models.ForeignKey(Organisation,on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    file = models.FileField(upload_to='org_external/', null=True)
    filename = models.CharField(max_length=100, null=True)
    status = models.BooleanField(null=True)