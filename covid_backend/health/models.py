from django.db import models
from patient.models import *
from user.models import *
from patient.models import *
# Create your models here.


class HealthStatus(TimeStamped):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    oxy_level = models.IntegerField(blank=False, null=False)
    blood_pres_systolic = models.IntegerField(blank=False, null=False)
    blood_pres_diastolic = models.IntegerField(blank=False, null=False)
    temperature = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return "Pat : {0} ,OL : {1}, T : {2}C ".format(self.patient.name, self.oxy_level, self.temperature)

