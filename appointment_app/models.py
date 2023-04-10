from django.db import models

from user_management.models import User


# Create your models here.


class   Appointment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="patient")
    counsellor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="counsellor")
    date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.patient.email
    

    class Meta:
        db_table = 'appointment_db'
        ordering = ['-created_at']
        verbose_name_plural = "Appointments"