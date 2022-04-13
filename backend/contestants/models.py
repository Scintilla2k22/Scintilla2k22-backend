from asyncio import events
from statistics import mode
from tabnanny import verbose
from django.db import models
from backend.utils.time_stamp import *
# from events.models import Events
# Create your models here.



class Contestants(TimeStamped):
    BRANCH_CHOICE = (
        ("CSE", ("Computer Science and Engineering")),
        ("MEC", ("FEMALE")),
        ("ECE", ("OTHERS")),
        ("CHE", ("OTHERS")),
        ("EE", ("OTHERS")),
        ("CIV", ("OTHERS")),
    )
    YEAR = (
        ( 1, "1st year"),
        ( 2, "2nd year"),
        ( 3, "3rd year"),
        ( 4, "4th year"),

    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=240, null=False, blank=False)
    contact_number = models.IntegerField(blank=True, null=True)
    branch = models.CharField( max_length = 244, choices=BRANCH_CHOICE)
    year = models.SmallIntegerField(choices=YEAR)
    event = models.ManyToManyField("events.Events",  blank=True)
    score = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    class Meta:
        verbose_name = "Contestant"

    def __str__(self):
        return "Contestant : {0}, ID : {1}".format(self.name, self.id)




class Teams(TimeStamped):
    t_name = models.CharField(max_length=244)
    contestants = models.ManyToManyField(Contestants, blank = True)
    event = models.ForeignKey("events.Events", on_delete=models.CASCADE, blank=False, null=False)
    score = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    class Meta:
        verbose_name = "Team"

    def __str__(self):
        return "Team : {0} - {1} ".format(self.t_name, self.event.e_name)
