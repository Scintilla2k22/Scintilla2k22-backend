from sre_parse import Verbose
from statistics import mode
from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import User
from contestants.models import *
from backend.utils.time_stamp import *
from django.contrib.auth.models import AbstractUser


class Coordinators(AbstractUser):
    BRANCH_CHOICE = (
        ("CSE", ("Computer Science and Engineering")),
        ("MEC", ("Mechanical Engineering")),
        ("ECE", ("Electronics and Communication")),
        ("CHE", ("Chemical Engineering")),
        ("EE", ("OTHERS")),
        ("CIV", ("OTHERS")),
    )
    YEAR = (
        ( 1, "1st year"),
        ( 2, "2nd year"),
        ( 3, "3rd year"),
        ( 4, "4th year"),

    )
    GENDER_CHOICE = (
    ("M", ("MALE")),
    ("F", ("FEMALE")),
    ("O", ("OTHERS"))
    )
    username = models.CharField(max_length=255, unique=True, blank=False, null=False)   
    contact_number = models.IntegerField(blank=True, null=True)
    branch = models.CharField( max_length = 244, choices=BRANCH_CHOICE)
    year = models.SmallIntegerField(choices=YEAR)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICE, null=True, blank=True)



class Events(TimeStamped):
    CHOICES = (
    (0, 'solo' ),
    (1, 'team')
    )
    EVENT_STATUS = (
    (1, 'comming soon' ),
    (2, 'live'),
    (3, 'ended')
    )
    id = models.IntegerField(primary_key=True)
    e_name = models.CharField(max_length=255, blank=False, null=False, verbose_name="Event Name")
    e_desc = models.TextField(blank=True, verbose_name="Description")
    co_ord = models.ManyToManyField(User,   verbose_name= "Co-ordinators", blank=True)
    type = models.SmallIntegerField(choices=CHOICES, verbose_name= "Type")
    status = models.SmallIntegerField(choices = EVENT_STATUS, default = 0)
    e_time = models.DateTimeField(auto_now_add = False, auto_now = False)
    image = models.ImageField(upload_to='image/events/', blank=True, null=True)
    url = models.URLField(null=True, blank=True)    
    code = models.CharField(max_length=200, blank=True, null=True)
    class Meta:
        verbose_name = "Event"
    

    def __str__(self):
        return "event - {0} - {1} - {2}".format(self.e_name, self.code, self.get_status_display())
    
   