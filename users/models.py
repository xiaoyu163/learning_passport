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

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    matric_no = models.CharField(max_length=10)
    enrol_year = models.DateField()
    grad_year = models.DateField()
    Program = (
        (1, "Bachelor of Arts Chinese Studies"),
        (2, "Master of Chinese Studies (Coursework)"),
        (3, "Master of Arts (Research)"),
        (4, "Doctor of Philosophy (Ph.D)"),
    )
    program = models.SmallIntegerField(choices=Program)
    
class Teacher(models.Model):
    lecturer = models.OneToOneField(User, on_delete=models.PROTECT)
    students = models.ManyToManyField(Student)
    Position = (
        (1, "Adjunct Professor"),
        (2, "Associate Professor"),
        (3, "Senior Lecturer"),
        (4, "Lecturer"),
        (5, "Post Doctoral Research Fellow"),       
    )
    position = models.SmallIntegerField(choices=Position)

class Organisation(models.Model):
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    internal = models.BooleanField()
    file = models.FileField(upload_to="org_com/")
    