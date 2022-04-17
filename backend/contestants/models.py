from django.db import models
from backend.utils.time_stamp import *
# from events.models import Events
# Create your models here.


class Score(TimeStamped):
    score = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    event = models.ForeignKey("events.Events",related_name="event_score", on_delete=models.CASCADE, blank=True, null=True)


class Contestants(TimeStamped):
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
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=240, null=False, blank=False)
    contact_number = models.IntegerField(blank=True, null=True)
    branch = models.CharField( max_length = 244, choices=BRANCH_CHOICE)
    year = models.SmallIntegerField(choices=YEAR)
    events = models.ManyToManyField("events.Events",related_name="events", blank=True)
    score = models.ForeignKey(Score, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "Contestant"

    def __str__(self):
        return "Contestant : {0}, ID : {1}".format(self.name, self.id)




class Teams(TimeStamped):
    t_name = models.CharField(max_length=244)
    contestants = models.ManyToManyField(Contestants, blank = True)
    event = models.ForeignKey("events.Events", on_delete=models.SET_NULL, blank=True, null=True)
    image = models.ImageField(upload_to='image/teams/', blank=True, null=True)
    score = models.ForeignKey(Score, on_delete=models.CASCADE, null=True, blank=True )
    
    
    class Meta:
        verbose_name = "Team"

    def __str__(self):
        return "Team : {0} - {1} ".format(self.t_name, self.event.e_name)
