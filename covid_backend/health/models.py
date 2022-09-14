from patient.models import PatientProfile
from django.db import models
from patient.models import *
from user.models import *
from patient.models import *
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from django.db.models.signals import pre_delete, post_save, post_delete
from django.utils.translation import gettext_lazy as _

# Create your models here.


class HealthStatus(TimeStamped):
    PATIENT_CONDITION = (
        ("1", ("Asymptomataic")),
        ("2", ("Mild")),
        ("3", ("Moderate")),
        ("4", ("Severe"))
    )

    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    patient_condition = models.CharField(choices=PATIENT_CONDITION, max_length=50)
    oxy_level = models.IntegerField(blank=False, null=False)
    blood_pres_systolic = models.IntegerField(blank=False, null=False)
    blood_pres_diastolic = models.IntegerField(blank=False, null=False)
    pulse_rate = models.IntegerField(blank=False, null=False)
    respiration_rate = models.IntegerField(blank=True, null=True)
    temperature = models.DecimalField(blank=False, null=False, max_digits=8, decimal_places=2)
    class Meta:
        verbose_name = _("Health Status")
        verbose_name_plural = _("Health Status")
        ordering = ['-created_on']

    def __str__(self):
        return "Patient : {0} | PC : {1} | OL : {2}% | BP : {3}/{4} mm Hg | PR : {5}bpm | T : {6}F | RR : {7} ".format(self.patient.patient_id,self.get_patient_condition_display(), \
        self.oxy_level, self.blood_pres_systolic, self.blood_pres_diastolic, self.pulse_rate, self.temperature, self.respiration_rate)

    @property
    def get_patient_condition(self):
        return self.get_patient_condition_display()

    @property
    def get_current_health(self):
        return {
            "OL" : self.oxy_level,
            # "BP" : f"{self.blood_pres_systolic}/{self.blood_pres_diastolic}",
            "PR" : self.pulse_rate,
            "RR" : self.respiration_rate,
            "T" : self.temperature
        }
        

@receiver(post_save, sender=HealthStatus)
def update_health_condition(sender, instance=None, created=False, **kwargs):
    if created:
        patient = get_object_or_404(PatientProfile, patient_id= instance.patient.patient_id)
        patient.health_condition = instance.patient_condition
        patient.save()