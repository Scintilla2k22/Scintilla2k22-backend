from sre_parse import Verbose
from statistics import mode
from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import User
from contestants.models import *
from backend.utils.time_stamp import *




class Events(TimeStamped):
    CHOICES = (
    (0, 'solo' ),
    (1, 'team')
    )
    EVENT_STATUS = (
    (0, 'comming soon' ),
    (2, 'live'),
    (3, 'ended')
    )
    id = models.AutoField(primary_key=True)
    e_name = models.CharField(max_length=255, blank=False, null=False, verbose_name="Event Name")
    e_desc = models.TextField(blank=True, verbose_name="Description")
    co_ord = models.ManyToManyField(User,   verbose_name= "Co-ordinators", blank=True)
    type = models.SmallIntegerField(choices=CHOICES, verbose_name= "Type")
    status = models.SmallIntegerField(choices = EVENT_STATUS, default = 0)
    e_time = models.DateTimeField(auto_now_add = False, auto_now = False)
    image = models.ImageField(upload_to='image/events/', blank=True, null=True)
    
    class Meta:
        verbose_name = "Event"
    

    def __str__(self):
        return "event - {0} - {1}".format(self.e_name, self.get_status_display())
    
   