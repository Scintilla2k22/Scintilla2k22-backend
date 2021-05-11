from django.db import models
from patient.models import *
from user.models import *
from patient.models import *
# Create your models here.

class Bed(TimeStamped):
    BED_CAT = (
        ("1", ("General Bed")),
        ("2", ("Oxygen Bed")),
        ('3', ("ICU Bed")),
        ('4', ("Ventillator Bed"))
    )
    bed_number = models.IntegerField(null=False, blank=False)
    bed_category = models.CharField(choices=BED_CAT, max_length=30)
    bed_status = models.BooleanField(default=False)

    def __str__(self):
        return "{0} ,  Status : {1}".format(self.get_bed_category_display(), "Taken" if self.bed_status  else "Free")


class BedStatus(Bed):
    bed_status = True
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return "{0} , patient : {1}".format(self.get_bed_category_display(), self.patient.username)

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

