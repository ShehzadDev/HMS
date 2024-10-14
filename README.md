

## Queries

Retrieve all patients admitted on a specific date.

```bash
Patient.objects.filter(date_admitted__date=specific_date)
```

Get the names of all doctors who have patients with a specific diagnosis.

```bash
Doctor.objects.filter(patients__medical_records__diagnoses__icontains=diagnosis).distinct().values_list("name", flat=True)
```
Find all patients treated by a particular nurse.
```
Patient.objects.filter(nurse_id=nurse_id)
```
Retrieve the contact number of the doctor for a given patient.


```
Doctor.objects.filter(patients__id=patient_id).values_list("contact_number", flat=True)
```
Get the total number of patients admitted to the hospital.
```
Patient.objects.count()
```
Retrieve the names of nurses who have patients with a specific prescription.
```
Nurse.objects.filter(patients__medical_records__prescription__icontains=specific_prescription).distinct().values_list("name", flat=True)
```
Get the average age of patients in the hospital.
```
Patient.objects.aggregate(Avg("age"))
```
Find the most recently admitted patient.
```
Patient.objects.latest("date_admitted")
```
Retrieve all doctors who have more than five patients.
```
Doctor.objects.annotate(num_patients=Count("patients")).filter(num_patients__gt=5)
```
Find the patients who have been admitted for more than a week.
```
Patient.objects.filter(date_admitted__lte=timezone.now() - timedelta(weeks=1)
```
Get the number of patients assigned to each nurse.
```
Nurse.objects.annotate(num_patients=Count("patients")).values("name", "num_patients")
```
Retrieve the names of patients who have a specific doctor.
```
Patient.objects.filter(doctor=Doctor.objects.get(id=doctor_id))
```
Find the doctors who specialize in a specific medical field.
```
Doctor.objects.filter(specialization__icontains=specific_specialization
```
Get the names of patients treated by a doctor with a specific specialization.
```
Patient.objects.filter(doctor__specialization__icontains=specific_specialization)
```
Find the nurses who have not been assigned any patients.
```
Nurse.objects.filter(patients__isnull=True)
```
Retrieve the latest medical record for a given patient.
```
MedicalRecord.objects.filter(patient=Patient.objects.get(id=patient_id)).latest("id")
```
Get the names of patients with a specific diagnosis.
```
Patient.objects.filter(medical_records__diagnoses__icontains=specific_diagnosis).distinct()
```
Find the doctors who have patients of a certain age group.
```
Doctor.objects.filter(patients__age__gte=min_age, patients__age__lte=max_age).distinct()
```
Retrieve all patients with a specific prescription.
```
Patient.objects.filter(medical_records__prescription__icontains=specific_prescription).distinct()
```
Find the nurses who have patients with a specific age.
```
Nurse.objects.filter(patients__age=specific_age).distinct()
```
Get the total number of medical records in the system.
```
MedicalRecord.objects.count()
```
Retrieve the names of patients treated by a nurse with a specific contact number.
```
Patient.objects.filter(nurse__contact_number=specific_contact_number)
```
Find the patients who are treated by more than one doctor.
```
Patient.objects.annotate(num_doctors=Count("doctor")).filter(num_doctors__gt=1)
```
Get the names of doctors who have treated patients with a specific prescription.
```
Doctor.objects.filter(patients__medical_records__prescription__icontains=specific_prescription).distinct().values_list("name", flat=True)
```
Find the patients who have not been assigned to any doctor.
```
Patient.objects.filter(doctor__isnull=True)
```
Retrieve the doctors who have patients admitted on a specific date.
```
Doctor.objects.filter(patients__date_admitted__date=specific_date).distinct()
```
Get the number of patients admitted each month.

```
Patient.objects.annotate(month=TruncMonth("date_admitted")).values("month").annotate(count=Count("id")).order_by("month")
```
Find the patients with the highest age in the hospital.

```
Patient.objects.order_by("-age").first()
```
Retrieve all nurses who have patients admitted on a specific date.

```
Nurse.objects.filter(patients__date_admitted__date=specific_date).distinct()
```
Find the doctors who have patients with a specific age.

```
Doctor.objects.filter(patients__age=specific_age).distinct()
```

Get the number of patients treated by each doctor.
```
Doctor.objects.annotate(num_patients=Count("patients")).values("name", "num_patients")
```
Retrieve the names of patients with a specific ag
```
Patient.objects.filter(age=specific_age).values_list("name", flat=True)
```
Find the nurses who have patients with a specific diagnosis.
```
Nurse.objects.filter(patients__medical_records__diagnoses__icontains=specific_diagnosis).distinct()
```
Find the doctors who have not been assigned any patients.
```
Doctor.objects.filter(patients__isnull=True).distinct()
```

Retrieve the patients who have medical records with a specific prescription.
```
Patient.objects.filter(medical_records__prescription__icontains=specific_prescription).distinct()
```
Get the average age of patients treated by each doctor.

```
Doctor.objects.annotate(avg_age=Avg("patients__age")).values("name", "avg_age")
```
Find the doctors who have patients with a specific prescription.
```
Doctor.objects.filter(patients__medical_records__prescription__icontains=specific_prescription).distinct()
```
Retrieve the names of patients treated by a doctor with a specific contact number.
```
Patient.objects.filter(doctor__contact_number=specific_contact_number).values_list("name", flat=True)
```
Find the nurses who have patients with a specific prescription.
```
Nurse.objects.filter(patients__medical_records__prescription__icontains=specific_prescription).distinct()
```
 Get the total number of patients treated by nurses in a specific specialization.
```
Nurse.objects.filter(patients__doctor__specialization__icontains=specific_specialization).annotate(num_patients=Count("patients")).values("name", "num_patients")
```
Retrieve the patients who have not been assigned to any nurse.
```
Patient.objects.filter(nurse__isnull=True)
```
Find the doctors who have patients admitted for more than a week.
```
Doctor.objects.filter(patients__date_admitted__lte=timezone.now() - timedelta(weeks=1)).distinct()
```
Get the names of patients with a specific diagnosis treated by a specific doctor.
```
Patient.objects.filter(doctor=Doctor.objects.get(id=doctor_id),medical_records__diagnoses__icontains=specific_diagnosis,).distinct().values_list("name", flat=True)
```
Find the nurses who have patients with a specific age group.
```
Nurse.objects.filter(patients__age__gte=min_age, patients__age__lte=max_age).distinct()
```
Retrieve the doctors who have patients with a specific diagnosis and age group.
```
Doctor.objects.filter(
patients__medical_records__diagnoses__icontains=specific_diagnosis,
patients__age__gte=min_age,
patients__age__lte=max_age,
).distinct()
```
Get the number of patients treated by each nurse in a specific specialization.
```
Nurse.objects.filter(patients__doctor__specialization__icontains=specific_specialization).annotate(num_patients=Count("patients")).values("name", "num_patients")
```
Find the patients who have been treated by more than one nurse.
```
Patient.objects.annotate(num_nurses=Count("nurse")).filter(num_nurses__gt=1)
```
Retrieve the names of doctors who have patients with a specific diagnosis and age group
```
Doctor.objects.filter(
patients__medical_records__diagnoses__icontains=specific_diagnosis,
patients__age__gte=min_age,
patients__age__lte=max_age,
).distinct()
.values_list("name", flat=True)
```



Select all patients with their associated doctors and nurses.
```bash
Patient.objects.prefetch_related("doctor", "nurse").all()
```

Select all patients admitted after a specific date.
```bash
Patient.objects.filter(date_admitted__gt=specific_date)
```
3. Count the total number of patients.
```bash
Patient.objects.count()
```

Count the total number of patients with a specific age.
```bash
Patient.objects.filter(age=specific_age).count()
```

Select all patients with their associated doctors and nurses.
```bash
Patient.objects.prefetch_related("doctor", "nurse").all()
```

Count the total number of doctors associated with each patient.
```bash
Patient.objects.annotate(doctor_count=Count("doctor")).all()
```

Sum the ages of all patients.
```bash
Patient.objects.aggregate(Sum("age"))
```

Select all patients along with the number of doctors associated with each.
```bash
Patient.objects.annotate(doctor_count=Count("doctor")).all()
```

Select all patients along with their medical records, if available.
```bash
Patient.objects.prefetch_related("medical_records").all()
```
Count the total number of nurses associated with each patient.
```bash
Patient.objects.annotate(nurse_count=Count("nurse")).all()
```

Select all patients with their associated nurses and the nurses' contact numbers.
```bash
Patient.objects.prefetch_related("nurse").all()
```

Select all patients along with the total number of medical records for each.
```bash
Patient.objects.annotate(medical_record_count=Count("medical_records")).all()
```

Select all patients with their diagnoses and prescriptions, if available.
```bash
Patient.objects.prefetch_related("medical_records").all()
```

Count the total number of patients admitted in a specific year.
```bash
Patient.objects.filter(date_admitted__year=specific_year).count()
```

Select all patients along with their doctors' specializations.
```bash
Patient.objects.prefetch_related("doctor").all()
```
Select all patients along with the count of medical records for each.
```bash
Patient.objects.annotate(medical_record_count=Count("medical_records")).all()
```

Select all doctors with the count of patients they are associated with.
```bash
Doctor.objects.annotate(patient_count=Count("patients")).all()
```

Select all patients along with the count of nurses they are associated with.
```bash
Patient.objects.annotate(nurse_count=Count("nurse")).all()
```

Annotate the average age of patients.
```bash
Patient.objects.aggregate(average_age=Avg("age"))
```

Annotate the maximum age of patients.
```bash
Patient.objects.aggregate(max_age=Max("age"))
```

Annotate the minimum age of patients.
```bash
Patient.objects.aggregate(min_age=Min("age"))
```

Select all patients along with the earliest admission date.
```bash
Patient.objects.order_by("date_admitted").first()
```

Select all doctors with their associated patients prefetched.
```bash
Doctor.objects.prefetch_related("patients").all()
```

Select all nurses with their associated patients prefetched.
```bash
Nurse.objects.prefetch_related("patients").all()
```
Select all patients along with the count of distinct doctors they are associated with.
```bash
Patient.objects.annotate(distinct_doctor_count=Count("doctor", distinct=True)).all()
```
