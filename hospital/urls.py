"""
URL configuration for hospital project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("api.urls")),
    path("diagnosis", include("api.urls")),
    path("patients", include("api.urls")),
    path("doctor_contact", include("api.urls")),
    path("total", include("api.urls")),
    path("nurse_presp", include("api.urls")),
    path("average_age", include("api.urls")),
    path("latest_patient", include("api.urls")),
    path("busy_doctors", include("api.urls")),
    path("long_term_patients", include("api.urls")),
    path("nurse_patient_count", include("api.urls")),
    path("patients_by_doctor", include("api.urls")),
    path("specialization", include("api.urls")),
    path("patients_by_specialization", include("api.urls")),
    path("unassigned_nurses", include("api.urls")),
    path("latest_medical_record", include("api.urls")),
    path("patients_with_diagnosis", include("api.urls")),
    path("doctors_by_age_group", include("api.urls")),
    path("patients_with_prescription", include("api.urls")),
    path("nurses_by_patient_age", include("api.urls")),
    path("total_medical_records", include("api.urls")),
    path("patients_by_nurse_contact", include("api.urls")),
    path("patients_with_multiple_doctors", include("api.urls")),
    path("doctors_by_prescription", include("api.urls")),
]
