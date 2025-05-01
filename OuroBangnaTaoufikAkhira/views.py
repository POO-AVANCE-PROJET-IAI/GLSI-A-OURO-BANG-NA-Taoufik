from django.shortcuts import render, get_object_or_404, redirect
from .models import Patient, ActType, Act, Medicine
from django.contrib import messages


def home(request):
    return render(request, "home.html")


# ========================================
# ============= Patients =================
# ========================================
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


# ========================================
# =========== Types d'actes ==============
# ========================================


def generate_acttype_code():
    last_acttype = ActType.objects.order_by("id").last()
    if not last_acttype:
        return "T-ACT-001"
    last_code = last_acttype.code
    code_number = int(last_code.split("-")[-1]) + 1
    return f"T-ACT-{code_number:03}"


def acttype_index(request):
    acttypes = ActType.objects.all()
    return render(request, "acttypes/index.html", {"acttypes": acttypes})


def acttype_show(request, pk):
    acttype = get_object_or_404(ActType, pk=pk)
    return render(request, "acttypes/show.html", {"acttype": acttype})


def acttype_create(request):
    return render(request, "acttypes/create.html")


def acttype_store(request):
    if request.method == "POST":
        code = generate_acttype_code()
        libelle = request.POST.get("libelle")

        if ActType.objects.filter(libelle=libelle).exists():
            messages.error(request, "Ce type d'acte médical existe déjà.")
            return redirect("acttypes.create")

        ActType.objects.create(code=code, libelle=libelle)
        return redirect("acttypes.index")


def acttype_edit(request, pk):
    acttype = get_object_or_404(ActType, pk=pk)
    return render(request, "acttypes/edit.html", {"acttype": acttype})


def acttype_update(request, pk):
    acttype = get_object_or_404(ActType, pk=pk)
    if request.method == "POST":
        libelle = request.POST.get("libelle")
        acttype.libelle = libelle
        acttype.save()
        return redirect("acttypes.index")


def acttype_destroy(request, pk):
    acttype = get_object_or_404(ActType, pk=pk)
    acttype.delete()
    return redirect("acttypes.index")


# ========================================
# =============== Acts ===================
# ========================================
def generate_act_code():
    last_act = Act.objects.order_by("id").last()
    if not last_act:
        return "ACT-001"
    last_code = last_act.code
    code_number = int(last_code.split("-")[-1]) + 1
    return f"ACT-{code_number:03}"


def act_index(request):
    acts = Act.objects.all()
    return render(request, "acts/index.html", {"acts": acts})


def act_show(request, pk):
    act = get_object_or_404(Act, pk=pk)
    return render(request, "acts/show.html", {"act": act})


def act_create(request):
    act_types = ActType.objects.all()
    return render(request, "acts/create.html", {"act_types": act_types})


def act_store(request):
    if request.method == "POST":
        libelle = request.POST.get("libelle")
        amount = request.POST.get("amount")
        act_type_id = request.POST.get("act_type")

        if Act.objects.filter(libelle=libelle).exists():
            messages.error(request, "Libelle already exists.")
            return redirect("acts.create")

        code = generate_act_code()

        act_type = get_object_or_404(ActType, pk=act_type_id)
        Act.objects.create(code=code, libelle=libelle, amount=amount, act_type=act_type)
        return redirect("acts.index")


def act_edit(request, pk):
    act = get_object_or_404(Act, pk=pk)
    act_types = ActType.objects.all()
    return render(request, "acts/edit.html", {"act": act, "act_types": act_types})


def act_update(request, pk):
    act = get_object_or_404(Act, pk=pk)
    if request.method == "POST":
        libelle = request.POST.get("libelle")
        amount = request.POST.get("amount")
        act_type_id = request.POST.get("act_type")

        if Act.objects.filter(libelle=libelle).exclude(pk=pk).exists():
            messages.error(request, "Libelle already exists.")
            return redirect("acts.edit", pk=pk)

        act_type = get_object_or_404(ActType, pk=act_type_id)
        act.libelle = libelle
        act.amount = amount
        act.act_type = act_type
        act.save()
        return redirect("acts.index")


def act_destroy(request, pk):
    act = get_object_or_404(Act, pk=pk)
    act.delete()
    return redirect("acts.index")


# ========================================
# ============= Medicaments ==============
# ========================================


def generate_medicine_code():
    last_medicine = Medicine.objects.order_by("id").last()
    if not last_medicine:
        return "MDCN-001"
    last_code = last_medicine.code
    code_number = int(last_code.split("-")[-1]) + 1
    return f"MDCN-{code_number:03}"


def medicine_index(request):
    medicines = Medicine.objects.all()
    return render(request, "medicines/index.html", {"medicines": medicines})


def medicine_show(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    return render(request, "medicines/show.html", {"medicine": medicine})


def medicine_create(request):
    return render(request, "medicines/create.html")


def medicine_store(request):
    if request.method == "POST":
        libelle = request.POST.get("libelle")

        if Medicine.objects.filter(libelle=libelle).exists():
            messages.error(request, "Libelle already exists.")
            return redirect("medicines.create")

        code = generate_medicine_code()

        Medicine.objects.create(code=code, libelle=libelle)
        return redirect("medicines.index")


def medicine_edit(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    return render(request, "medicines/edit.html", {"medicine": medicine})


def medicine_update(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    if request.method == "POST":
        libelle = request.POST.get("libelle")

        if Medicine.objects.filter(libelle=libelle).exclude(pk=pk).exists():
            messages.error(request, "Libelle already exists.")
            return redirect("medicines.edit", pk=pk)

        medicine.libelle = libelle
        medicine.save()
        return redirect("medicines.index")


def medicine_destroy(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    medicine.delete()
    return redirect("medicines.index")
