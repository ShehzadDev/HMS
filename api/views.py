from datetime import datetime, timedelta

from django.db.models import Avg, Count, Max, Min, Sum
from django.db.models.functions import TruncMonth
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .models import Doctor, MedicalRecord, Nurse, Patient

# Create your views here.


@csrf_exempt
def index(request):
    if request.method == "POST":
        specific_date = request.POST.get("date")
        if specific_date:
            specific_date = datetime.strptime(specific_date, "%Y-%m-%d").date()
        else:
            specific_date = datetime.now().date()
    else:
        specific_date = datetime.now().date()

    patients = Patient.objects.filter(date_admitted__date=specific_date)
    return render(request, "index.html", {"patients": patients})


@csrf_exempt
def diagnosis(request):
    if request.method == "POST":
        diagnosis = request.POST.get("diagnosis")
        if diagnosis:
            doctors = (
                Doctor.objects.filter(
                    patients__medical_records__diagnoses__icontains=diagnosis
                )
                .distinct()
                .values_list("name", flat=True)
            )
        else:
            doctors = []
    else:
        doctors = []

    return render(request, "index.html", {"doctors": doctors})


@csrf_exempt
def patients(request):
    nurses = Nurse.objects.all()

    if request.method == "POST":
        nurse_id = request.POST.get("nurse_id")
        if nurse_id:
            try:
                nurse_instance = Nurse.objects.get(id=nurse_id)
                patients = Patient.objects.filter(nurse=nurse_instance)
            except Nurse.DoesNotExist:
                patients = []
        else:
            patients = []
    else:
        patients = []

    return render(request, "index.html", {"nurses": nurses, "nurse_patients": patients})


@csrf_exempt
def contacts(request):
    patients = Patient.objects.all()

    if request.method == "POST":
        patient_id = request.POST.get("patient_id")
        if patient_id:
            try:
                patient_instance = Patient.objects.get(id=patient_id)
                contact_numbers = Doctor.objects.filter(
                    patients=patient_instance
                ).values_list("contact_number", flat=True)
            except Patient.DoesNotExist:
                contact_numbers = []
        else:
            contact_numbers = []
    else:
        contact_numbers = []

    return render(
        request,
        "index.html",
        {"contact_numbers": contact_numbers, "patient_doc": patients},
    )


@csrf_exempt
def total(request):
    total = Patient.objects.count()
    return render(request, "index.html", {"total": total})


@csrf_exempt
def nurse_presp(request):
    if request.method == "POST":
        specific_prescription = request.POST.get("prescription")
        if specific_prescription:
            nurses = (
                Nurse.objects.filter(
                    patients__medical_records__prescription__icontains=specific_prescription
                )
                .distinct()
                .values_list("name", flat=True)
            )
        else:
            nurses = []
    else:
        nurses = []

    return render(request, "index.html", {"nurses_pres": nurses})


@csrf_exempt
def average_age(request):
    average_age = Patient.objects.aggregate(Avg("age"))["age__avg"]
    return render(request, "index.html", {"average_age": average_age})


@csrf_exempt
def latest_patient(request):
    try:
        latest_patient = Patient.objects.latest("date_admitted")
    except Patient.DoesNotExist:
        latest_patient = None

    return render(request, "index.html", {"latest_patient": latest_patient})


@csrf_exempt
def busy_doctors(request):
    busy_doctors = Doctor.objects.annotate(num_patients=Count("patients")).filter(
        num_patients__gt=5
    )
    return render(request, "index.html", {"busy_doctors": busy_doctors})


@csrf_exempt
def long_term_patients(request):
    long_term_patients = Patient.objects.filter(
        date_admitted__lte=timezone.now() - timedelta(weeks=1)
    )
    return render(request, "index.html", {"long_term_patients": long_term_patients})


@csrf_exempt
def nurse_patient_count(request):
    nurse_patient_counts = Nurse.objects.annotate(
        num_patients=Count("patients")
    ).values("name", "num_patients")
    return render(request, "index.html", {"nurse_patient_counts": nurse_patient_counts})


@csrf_exempt
def patients_by_doctor(request):
    doctors = Doctor.objects.all()
    if request.method == "POST":
        doctor_id = request.POST.get("doctor_id")
        if doctor_id:
            try:
                doctor_instance = Doctor.objects.get(id=doctor_id)
                patient_names = Patient.objects.filter(
                    doctor=doctor_instance
                ).values_list("name", flat=True)
            except Doctor.DoesNotExist:
                patient_names = []
        else:
            patient_names = []
    else:
        patient_names = []

    return render(
        request, "index.html", {"patient_names": patient_names, "doctors": doctors}
    )


@csrf_exempt
def specialization(request):
    doctors = Doctor.objects.all()
    specialized_doctors = []

    if request.method == "POST":
        specific_specialization = request.POST.get("specialization")
        if specific_specialization:
            specialized_doctors = Doctor.objects.filter(
                specialization__icontains=specific_specialization
            )

    return render(
        request,
        "index.html",
        {"doctors": doctors, "specialized_doctors": specialized_doctors},
    )


@csrf_exempt
def patients_by_specialization(request):
    doctors = Doctor.objects.all()
    patient_names = []

    if request.method == "POST":
        specific_specialization = request.POST.get("specialization")
        if specific_specialization:
            patient_names = Patient.objects.filter(
                doctor__specialization__icontains=specific_specialization
            ).values_list("name", flat=True)

    return render(
        request, "index.html", {"patient_names": patient_names, "doctors": doctors}
    )


@csrf_exempt
def unassigned_nurses(request):
    unassigned_nurses = Nurse.objects.filter(patients__isnull=True)
    return render(request, "index.html", {"unassigned_nurses": unassigned_nurses})


@csrf_exempt
def latest_medical_record(request):
    if request.method == "POST":
        patient_id = request.POST.get("patient_id")
        if patient_id:
            try:
                patient_instance = Patient.objects.get(id=patient_id)
                latest_record = MedicalRecord.objects.filter(
                    patient=patient_instance
                ).latest("id")
            except (Patient.DoesNotExist, MedicalRecord.DoesNotExist):
                latest_record = None
        else:
            latest_record = None
    else:
        latest_record = None

    return render(
        request,
        "index.html",
        {"latest_record": latest_record, "patients": Patient.objects.all()},
    )


@csrf_exempt
def patients_with_diagnosis(request):
    if request.method == "POST":
        specific_diagnosis = request.POST.get("diagnosis")
        if specific_diagnosis:
            patient_names = (
                Patient.objects.filter(
                    medical_records__diagnoses__icontains=specific_diagnosis
                )
                .distinct()
                .values_list("name", flat=True)
            )
        else:
            patient_names = []
    else:
        patient_names = []

    return render(request, "index.html", {"patient_names": patient_names})


@csrf_exempt
def doctors_by_age_group(request):
    if request.method == "POST":
        min_age = request.POST.get("min_age")
        max_age = request.POST.get("max_age")
        if min_age and max_age:
            doctors = Doctor.objects.filter(
                patients__age__gte=min_age, patients__age__lte=max_age
            ).distinct()
        else:
            doctors = []
    else:
        doctors = []

    return render(request, "index.html", {"doctors": doctors})


@csrf_exempt
def patients_with_prescription(request):
    if request.method == "POST":
        specific_prescription = request.POST.get("prescription")
        if specific_prescription:
            patients = Patient.objects.filter(
                medical_records__prescription__icontains=specific_prescription
            ).distinct()
        else:
            patients = []
    else:
        patients = []

    return render(request, "index.html", {"patients": patients})


@csrf_exempt
def nurses_by_patient_age(request):
    if request.method == "POST":
        specific_age = request.POST.get("age")
        if specific_age:
            nurses = Nurse.objects.filter(patients__age=specific_age).distinct()
        else:
            nurses = []
    else:
        nurses = []

    return render(request, "index.html", {"nurses": nurses})


@csrf_exempt
def total_medical_records(request):
    total_records = MedicalRecord.objects.count()
    return render(request, "index.html", {"total_records": total_records})


@csrf_exempt
def patients_by_nurse_contact(request):
    if request.method == "POST":
        specific_contact_number = request.POST.get("contact_number")
        if specific_contact_number:
            patient_names = Patient.objects.filter(
                nurse__contact_number=specific_contact_number
            ).values_list("name", flat=True)
        else:
            patient_names = []
    else:
        patient_names = []

    return render(request, "index.html", {"patient_names": patient_names})


@csrf_exempt
def patients_with_multiple_doctors(request):
    patients = Patient.objects.annotate(num_doctors=Count("doctor")).filter(
        num_doctors__gt=1
    )
    return render(request, "index.html", {"patients": patients})


@csrf_exempt
def doctors_by_prescription(request):
    if request.method == "POST":
        specific_prescription = request.POST.get("prescription")
        if specific_prescription:
            doctor_names = (
                Doctor.objects.filter(
                    patients__medical_records__prescription__icontains=specific_prescription
                )
                .distinct()
                .values_list("name", flat=True)
            )
        else:
            doctor_names = []
    else:
        doctor_names = []

    return render(request, "index.html", {"doctor_names": doctor_names})


@csrf_exempt
def unassigned_doctor_patients(request):
    unassigned_doctor_patients = Patient.objects.filter(doctor__isnull=True)
    return render(
        request,
        "index.html",
        {"unassigned_doctor_patients": unassigned_doctor_patients},
    )


@csrf_exempt
def doctors_by_admission_date(request):
    if request.method == "POST":
        specific_date = request.POST.get("date")
        if specific_date:
            specific_date = datetime.strptime(specific_date, "%Y-%m-%d").date()
            doctors = Doctor.objects.filter(
                patients__date_admitted__date=specific_date
            ).distinct()
        else:
            doctors = []
    else:
        doctors = []

    return render(request, "index.html", {"doctors": doctors})


@csrf_exempt
def patients_per_month(request):
    patients_per_month = (
        Patient.objects.annotate(month=TruncMonth("date_admitted"))
        .values("month")
        .annotate(count=Count("id"))
        .order_by("month")
    )
    print(patients_per_month)
    return render(request, "index.html", {"patients_per_month": patients_per_month})


@csrf_exempt
def oldest_patient(request):
    try:
        oldest_patient = Patient.objects.order_by("-age").first()
    except Patient.DoesNotExist:
        oldest_patient = None

    return render(request, "index.html", {"oldest_patient": oldest_patient})


@csrf_exempt
def nurses_by_admission_date(request):
    if request.method == "POST":
        specific_date = request.POST.get("date")
        if specific_date:
            specific_date = datetime.strptime(specific_date, "%Y-%m-%d").date()
            nurses = Nurse.objects.filter(
                patients__date_admitted__date=specific_date
            ).distinct()
        else:
            nurses = []
    else:
        nurses = []

    return render(request, "index.html", {"nurses": nurses})


@csrf_exempt
def doctors_by_patient_age(request):
    if request.method == "POST":
        specific_age = request.POST.get("age")
        if specific_age:
            doctors = Doctor.objects.filter(patients__age=specific_age).distinct()
        else:
            doctors = []
    else:
        doctors = []

    return render(request, "index.html", {"doctors": doctors})


@csrf_exempt
def doctor_patient_count(request):
    doctor_patient_counts = Doctor.objects.annotate(
        num_patients=Count("patients")
    ).values("name", "num_patients")
    return render(
        request, "index.html", {"doctor_patient_counts": doctor_patient_counts}
    )


@csrf_exempt
def patients_by_age(request):
    if request.method == "POST":
        specific_age = request.POST.get("age")
        if specific_age:
            patient_names = Patient.objects.filter(age=specific_age).values_list(
                "name", flat=True
            )
        else:
            patient_names = []
    else:
        patient_names = []

    return render(request, "index.html", {"patient_names": patient_names})


@csrf_exempt
def nurses_by_diagnosis(request):
    if request.method == "POST":
        specific_diagnosis = request.POST.get("diagnosis")
        if specific_diagnosis:
            nurses = Nurse.objects.filter(
                patients__medical_records__diagnoses__icontains=specific_diagnosis
            ).distinct()
        else:
            nurses = []
    else:
        nurses = []

    return render(request, "index.html", {"nurses": nurses})


@csrf_exempt
def unassigned_doctors(request):
    unassigned_doctors = Doctor.objects.filter(patients__isnull=True).distinct()
    return render(request, "index.html", {"unassigned_doctors": unassigned_doctors})


@csrf_exempt
def patients_with_specific_prescription(request):
    if request.method == "POST":
        specific_prescription = request.POST.get("prescription")
        if specific_prescription:
            patients = Patient.objects.filter(
                medical_records__prescription__icontains=specific_prescription
            ).distinct()
        else:
            patients = []
    else:
        patients = []

    return render(request, "index.html", {"patients": patients})


@csrf_exempt
def average_age_by_doctor(request):
    average_age_by_doctor = Doctor.objects.annotate(
        avg_age=Avg("patients__age")
    ).values("name", "avg_age")
    return render(
        request, "index.html", {"average_age_by_doctor": average_age_by_doctor}
    )


@csrf_exempt
def doctors_with_specific_prescription(request):
    if request.method == "POST":
        specific_prescription = request.POST.get("prescription")
        if specific_prescription:
            doctors = Doctor.objects.filter(
                patients__medical_records__prescription__icontains=specific_prescription
            ).distinct()
        else:
            doctors = []
    else:
        doctors = []

    return render(request, "index.html", {"doctors": doctors})


@csrf_exempt
def patients_by_doctor_contact(request):
    if request.method == "POST":
        specific_contact_number = request.POST.get("contact_number")
        if specific_contact_number:
            patient_names = Patient.objects.filter(
                doctor__contact_number=specific_contact_number
            ).values_list("name", flat=True)
        else:
            patient_names = []
    else:
        patient_names = []

    return render(request, "index.html", {"patient_names": patient_names})


@csrf_exempt
def nurses_by_prescription(request):
    if request.method == "POST":
        specific_prescription = request.POST.get("prescription")
        if specific_prescription:
            nurses = Nurse.objects.filter(
                patients__medical_records__prescription__icontains=specific_prescription
            ).distinct()
        else:
            nurses = []
    else:
        nurses = []

    return render(request, "index.html", {"nurses": nurses})


@csrf_exempt
def total_patients_by_specialization(request):
    if request.method == "POST":
        specific_specialization = request.POST.get("specialization")
        if specific_specialization:
            nurse_patient_counts = (
                Nurse.objects.filter(
                    patients__doctor__specialization__icontains=specific_specialization
                )
                .annotate(num_patients=Count("patients"))
                .values("name", "num_patients")
            )
        else:
            nurse_patient_counts = []
    else:
        nurse_patient_counts = []

    return render(request, "index.html", {"nurse_patient_counts": nurse_patient_counts})


@csrf_exempt
def unassigned_patients(request):
    unassigned_patients = Patient.objects.filter(nurse__isnull=True)
    return render(request, "index.html", {"unassigned_patients": unassigned_patients})


@csrf_exempt
def doctors_with_long_term_patients(request):
    long_term_doctors = Doctor.objects.filter(
        patients__date_admitted__lte=timezone.now() - timedelta(weeks=1)
    ).distinct()
    return render(request, "index.html", {"long_term_doctors": long_term_doctors})


@csrf_exempt
def patients_by_doctor_and_diagnosis(request):
    if request.method == "POST":
        doctor_id = request.POST.get("doctor_id")
        specific_diagnosis = request.POST.get("diagnosis")
        if doctor_id and specific_diagnosis:
            try:
                doctor_instance = Doctor.objects.get(id=doctor_id)
                patient_names = (
                    Patient.objects.filter(
                        doctor=doctor_instance,
                        medical_records__diagnoses__icontains=specific_diagnosis,
                    )
                    .distinct()
                    .values_list("name", flat=True)
                )
            except Doctor.DoesNotExist:
                patient_names = []
        else:
            patient_names = []
    else:
        patient_names = []

    return render(request, "index.html", {"patient_names": patient_names})


@csrf_exempt
def nurses_by_age_group(request):
    if request.method == "POST":
        min_age = request.POST.get("min_age")
        max_age = request.POST.get("max_age")
        if min_age and max_age:
            nurses = Nurse.objects.filter(
                patients__age__gte=min_age, patients__age__lte=max_age
            ).distinct()
        else:
            nurses = []
    else:
        nurses = []

    return render(request, "index.html", {"nurses": nurses})


@csrf_exempt
def doctors_by_diagnosis_and_age_group(request):
    if request.method == "POST":
        specific_diagnosis = request.POST.get("diagnosis")
        min_age = request.POST.get("min_age")
        max_age = request.POST.get("max_age")
        if specific_diagnosis and min_age and max_age:
            doctors = Doctor.objects.filter(
                patients__medical_records__diagnoses__icontains=specific_diagnosis,
                patients__age__gte=min_age,
                patients__age__lte=max_age,
            ).distinct()
        else:
            doctors = []
    else:
        doctors = []

    return render(request, "index.html", {"doctors": doctors})


@csrf_exempt
def nurse_patient_count_by_specialization(request):
    if request.method == "POST":
        specific_specialization = request.POST.get("specialization")
        if specific_specialization:
            nurse_patient_counts = (
                Nurse.objects.filter(
                    patients__doctor__specialization__icontains=specific_specialization
                )
                .annotate(num_patients=Count("patients"))
                .values("name", "num_patients")
            )
        else:
            nurse_patient_counts = []
    else:
        nurse_patient_counts = []

    return render(request, "index.html", {"nurse_patient_counts": nurse_patient_counts})


@csrf_exempt
def patients_with_multiple_nurses(request):
    patients = Patient.objects.annotate(num_nurses=Count("nurse")).filter(
        num_nurses__gt=1
    )
    return render(request, "index.html", {"patients": patients})


@csrf_exempt
def doctors_by_diagnosis_and_age_group_names(request):
    if request.method == "POST":
        specific_diagnosis = request.POST.get("diagnosis")
        min_age = request.POST.get("min_age")
        max_age = request.POST.get("max_age")
        if specific_diagnosis and min_age and max_age:
            doctor_names = (
                Doctor.objects.filter(
                    patients__medical_records__diagnoses__icontains=specific_diagnosis,
                    patients__age__gte=min_age,
                    patients__age__lte=max_age,
                )
                .distinct()
                .values_list("name", flat=True)
            )
        else:
            doctor_names = []
    else:
        doctor_names = []

    return render(request, "index.html", {"doctor_names": doctor_names})


@csrf_exempt
def home(request):

    patients_with_doctors_nurses = Patient.objects.prefetch_related(
        "doctor", "nurse"
    ).all()

    specific_date = timezone.datetime(2024, 10, 2)
    patients_admitted_after_date = Patient.objects.filter(
        date_admitted__gt=specific_date
    )

    total_patients = Patient.objects.count()

    specific_age = 32
    total_patients_with_age = Patient.objects.filter(age=specific_age)

    total_age_count = total_patients_with_age.count()

    total_age_sum = Patient.objects.aggregate(Sum("age"))

    patients_with_doctor_counts = Patient.objects.annotate(
        doctor_count=Count("doctor")
    ).all()

    patients_with_medical_records = Patient.objects.prefetch_related(
        "medical_records"
    ).all()

    patients_with_nurses_and_contacts = Patient.objects.prefetch_related("nurse").all()

    patients_with_medical_record_counts = Patient.objects.annotate(
        medical_record_count=Count("medical_records")
    ).all()

    # patients_with_diagnoses_prescriptions = Patient.objects.prefetch_related(
    # "medical_records"
    # ).all()

    specific_year = 2024
    total_patients_admitted_in_year = Patient.objects.filter(
        date_admitted__year=specific_year
    ).count()

    # patients_with_doctor_specializations = Patient.objects.prefetch_related(
    #     "doctor"
    # ).all()

    doctors_with_patient_counts = Doctor.objects.annotate(
        patient_count=Count("patients")
    ).all()

    # patients_with_nurse_counts = Patient.objects.annotate(
    #     nurse_count=Count("nurse")
    # ).all()

    average_patient_age = Patient.objects.aggregate(
        average_age=Sum("age") / Count("id")
    )

    max_patient_age = Patient.objects.aggregate(max_age=Max("age"))

    min_patient_age = Patient.objects.aggregate(min_age=Min("age"))

    earliest_admission_date = Patient.objects.order_by("date_admitted").first()

    doctors_with_patients = Doctor.objects.prefetch_related("patients").all()

    nurses_with_patients = Nurse.objects.prefetch_related("patients").all()

    patients_with_distinct_doctor_counts = Patient.objects.annotate(
        distinct_doctor_count=Count("doctor", distinct=True)
    ).all()

    return render(
        request,
        "home.html",
        {
            "patients_with_doctors_nurses": patients_with_doctors_nurses,
            "patients_admitted_after_date": patients_admitted_after_date,
            "total_patients": total_patients,
            "total_age_count": total_age_count,
            "total_patients_with_age": total_patients_with_age,
            "total_age_sum": total_age_sum,
            "patients_with_doctor_counts": patients_with_doctor_counts,
            "patients_with_medical_records": patients_with_medical_records,
            "patients_with_nurses_and_contacts": patients_with_nurses_and_contacts,
            "patients_with_medical_record_counts": patients_with_medical_record_counts,
            # "patients_with_diagnoses_prescriptions": patients_with_diagnoses_prescriptions,
            "total_patients_admitted_in_year": total_patients_admitted_in_year,
            # "patients_with_doctor_specializations": patients_with_doctor_specializations,
            "patients_with_medical_record_counts": patients_with_medical_record_counts,
            "doctors_with_patient_counts": doctors_with_patient_counts,
            # "patients_with_nurse_counts": patients_with_nurse_counts,
            "average_patient_age": average_patient_age,
            "max_patient_age": max_patient_age,
            "min_patient_age": min_patient_age,
            "earliest_admission_date": earliest_admission_date,
            "doctors_with_patients": doctors_with_patients,
            "nurses_with_patients": nurses_with_patients,
            "patients_with_distinct_doctor_counts": patients_with_distinct_doctor_counts,
        },
    )
