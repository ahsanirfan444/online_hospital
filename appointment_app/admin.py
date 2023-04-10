from django.contrib import admin
from appointment_app import models

# Register your models here.



class AppointmentssAdmin(admin.ModelAdmin):
    list_filter = ( 'patient',)
    search_fields = ('patient', 'counsellor', 'date',)


admin.site.register(models.Appointment, AppointmentssAdmin)


