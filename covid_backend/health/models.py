from django.db import models
from patient.models import *
from user.models import *
from patient.models import *
# Create your models here.


class HealthStatus(TimeStamped):
    PATIENT_CONDITION = (
        ("1", ("Asymptomataic")),
        ("2", ("Mild")),
        ("3", ("Moderate")),
        ("4", ("severe"))
    )

    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    patient_condition = models.CharField(choices=PATIENT_CONDITION, max_length=50)
    oxy_level = models.IntegerField(blank=False, null=False)
    blood_pres_systolic = models.IntegerField(blank=False, null=False)
    blood_pres_diastolic = models.IntegerField(blank=False, null=False)
    temperature = models.DecimalField(blank=False, null=False, max_digits=4, decimal_places=2)

    def __str__(self):
        return "Patient : {0} ,OL : {1}, T : {2}C ".format(self.patient.name, self.oxy_level, self.temperature)

