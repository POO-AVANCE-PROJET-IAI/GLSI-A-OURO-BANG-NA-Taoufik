from django.shortcuts import render, get_object_or_404, redirect
from .models import Patient
from django.contrib import messages


def home(request):
    return render(request, "home.html")

def patient_index(request):
    patients = Patient.objects.all()
    return render(request, "patient/index.html", {"patients": patients})

def patient_show(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    return render(request, "patient/show.html", {"patient": patient})

def patient_create(request):
    return render(request, "patient/create.html")

def patient_store(request):
    if request.method == "POST":
        last_name = request.POST.get("last_name")
        first_name = request.POST.get("first_name")
        phone_number = request.POST.get("phone_number")
        emergency_number = request.POST.get("emergency_number")
        adresse = request.POST.get("adresse")
        job = request.POST.get("job")

        if Patient.objects.filter(phone_number=phone_number).exists():
            messages.error(
                request,
                "Ce numéro de téléphone existe déjà. Veuillez en choisir un autre.",
            )
            return redirect("patients.create")

        if Patient.objects.filter(emergency_number=emergency_number).exists():
            messages.error(
                request,
                "Ce numéro d'urgence existe déjà. Veuillez en choisir un autre.",
            )
            return redirect("patients.create")

        Patient.objects.create(
            last_name=last_name,
            first_name=first_name,
            phone_number=phone_number,
            emergency_number=emergency_number,
            adresse=adresse,
            job=job,
        )
        return redirect("patients.index")

def patient_edit(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    return render(request, "patient/edit.html", {"patient": patient})

def patient_update(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == "POST":
        phone_number = request.POST.get("phone_number")
        emergency_number = request.POST.get("emergency_number")

        if Patient.objects.filter(phone_number=phone_number).exclude(pk=pk).exists():
            messages.error(
                request,
                "Ce numéro de téléphone existe déjà. Veuillez en choisir un autre.",
            )
            return redirect("patients.edit", pk=pk)

        if (
            Patient.objects.filter(emergency_number=emergency_number)
            .exclude(pk=pk)
            .exists()
        ):
            messages.error(
                request,
                "Ce numéro d'urgence existe déjà. Veuillez en choisir un autre.",
            )
            return redirect("patients.edit", pk=pk)

        patient.last_name = request.POST.get("last_name")
        patient.first_name = request.POST.get("first_name")
        patient.phone_number = phone_number
        patient.emergency_number = emergency_number
        patient.adresse = request.POST.get("adresse")
        patient.job = request.POST.get("job")
        patient.save()
        return redirect("patients.index")

def patient_destroy(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    patient.delete()
    return redirect("patients.index")


