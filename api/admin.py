from django.contrib import admin

from .models import Doctor, Hospital, MedicalRecord, Nurse, Patient

# Register your models here.
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Nurse)
admin.site.register(Hospital)
admin.site.register(MedicalRecord)
