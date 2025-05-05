from django.shortcuts import render, get_object_or_404, redirect
from .models import (
    Patient,
    ActType,
    Act,
    Medicine,
    Consultation,
    ConsultationDetails,
    User,
    Invoice,
    InvoiceDetails,
    Order,
    OrderDelails,
)
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.utils import timezone
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from django.db import models


def index(request):
    return render(request, "index.html")


# ========================================
# =============== Login ==================
# ========================================

@login_required(login_url="login")
def home(request):
    total_patients = Patient.objects.count()
    
    total_consultations = Consultation.objects.count()
    recent_consultations = Consultation.objects.order_by('-date')[:5]
    
    today = timezone.now().date()
    today_consultations = Consultation.objects.filter(date=today).count()
    
    total_invoices = Invoice.objects.count()
    paid_invoices = Invoice.objects.filter(status=True).count()
    unpaid_invoices = Invoice.objects.filter(status=False).count()
    
    payment_rate = 0
    if total_invoices > 0:
        payment_rate = (paid_invoices / total_invoices) * 100
    
    total_revenue = Invoice.objects.filter(status=True).aggregate(models.Sum('amount'))['amount__sum'] or 0
    
    popular_acts = ConsultationDetails.objects.values('act__libelle').annotate(
        count=models.Count('act')
    ).order_by('-count')[:5]
    
    popular_medicines = OrderDelails.objects.values('medicine__libelle').annotate(
        count=models.Count('medicine')
    ).order_by('-count')[:5]
    
    doctor_consultations = 0
    if not request.user.is_superuser:
        doctor_consultations = Consultation.objects.filter(doctor=request.user).count()
    
    context = {
        'total_patients': total_patients,
        'total_consultations': total_consultations,
        'recent_consultations': recent_consultations,
        'today_consultations': today_consultations,
        'total_invoices': total_invoices,
        'paid_invoices': paid_invoices,
        'unpaid_invoices': unpaid_invoices,
        'payment_rate': round(payment_rate, 2),
        'total_revenue': total_revenue,
        'popular_acts': popular_acts,
        'popular_medicines': popular_medicines,
        'doctor_consultations': doctor_consultations,
    }
    
    return render(request, "home.html", context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if hasattr(user, "status") and not user.status:
                messages.error(request, "Votre compte a été désactivé.")
                return render(request, "auth/login.html")

            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")

    return render(request, "auth/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


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


# ========================================
# =========== Consultations ==============
# ========================================
def generate_consultation_code():
    last_consultation = Consultation.objects.order_by("id").last()
    if not last_consultation:
        return "CONSULT-000001"
    last_code = last_consultation.code
    code_number = int(last_code.split("-")[-1]) + 1
    return f"CONSULT-{code_number:06}"


def generate_consultation_detail_code():
    last_detail = ConsultationDetails.objects.order_by("id").last()
    if not last_detail:
        return "CONSULT-DETAIL-000001"
    last_code = last_detail.code
    code_number = int(last_code.split("-")[-1]) + 1
    return f"CONSULT-DETAIL-{code_number:06}"


@login_required(login_url="login")
def consultation_create(request):
    if request.method == "POST":
        patient_id = request.POST.get("patient")
        act_id = request.POST.get("act")

        # Generate unique codes
        consultation_code = generate_consultation_code()
        detail_code = generate_consultation_detail_code()

        patient = get_object_or_404(Patient, pk=patient_id)
        act = get_object_or_404(Act, pk=act_id)

        # Ensure request.user is an instance of your custom User model
        doctor = get_object_or_404(User, pk=request.user.pk)

        consultation = Consultation.objects.create(
            code=consultation_code, doctor=doctor, patient=patient
        )

        ConsultationDetails.objects.create(
            code=detail_code, act=act, consultation=consultation
        )

        return redirect("consultations.index")

    patients = Patient.objects.all()
    acts = Act.objects.all()
    return render(
        request, "consultations/create.html", {"patients": patients, "acts": acts}
    )


@login_required(login_url="login")
def consultation_update(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    if request.method == "POST":
        act_id = request.POST.get("act")

        detail_code = generate_consultation_detail_code()

        act = get_object_or_404(Act, pk=act_id)

        ConsultationDetails.objects.create(
            code=detail_code, act=act, consultation=consultation
        )
        return redirect("consultations.index")

    acts = Act.objects.all()
    return render(
        request,
        "consultations/update.html",
        {"consultation": consultation, "acts": acts},
    )


@login_required(login_url="login")
def consultation_index(request):
    consultations = Consultation.objects.all()
    return render(request, "consultations/index.html", {"consultations": consultations})


@login_required(login_url="login")
def consultation_show(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    details = ConsultationDetails.objects.filter(consultation=consultation)
    return render(
        request,
        "consultations/show.html",
        {"consultation": consultation, "details": details},
    )


# ========================================
# =========== Factures ==============
# ========================================
def generate_invoice_code():
    now = timezone.now()
    year = now.year
    month = now.month
    last_invoice = (
        Invoice.objects.filter(code__startswith=f"FACT-{year}-{month:02d}-")
        .order_by("code")
        .last()
    )
    if not last_invoice:
        return f"FACT-{year}-{month:02d}-00001"
    last_number = int(last_invoice.code.split("-")[-1])
    new_number = last_number + 1
    return f"FACT-{year}-{month:02d}-{new_number:05d}"


def generate_invoice_detail_code():
    last_detail = InvoiceDetails.objects.order_by("id").last()
    if not last_detail:
        return "FACT-DETAIL-0000001"

    last_code = last_detail.code
    code_number = int(last_code.split("-")[-1]) + 1
    return f"FACT-DETAIL-{code_number:07d}"


@login_required(login_url="login")
def invoice_index(request):
    invoices = Invoice.objects.all()
    return render(request, "invoices/index.html", {"invoices": invoices})


@login_required(login_url="login")
def invoice_create(request):
    consultations = Consultation.objects.filter(invoice__isnull=True)

    if request.method == "POST":
        consultation_id = request.POST.get("consultation")
        consultation = get_object_or_404(Consultation, pk=consultation_id)

        invoice_code = generate_invoice_code()

        total_amount = 0
        consultation_details = ConsultationDetails.objects.filter(
            consultation=consultation
        )

        invoice = Invoice.objects.create(
            code=invoice_code,
            date=timezone.now(),
            amount=total_amount,
            user=request.user,
            status=False,
        )

        for detail in consultation_details:
            detail_code = generate_invoice_detail_code()
            act_amount = detail.act.amount
            total_amount += act_amount

            InvoiceDetails.objects.create(
                code=detail_code, invoice=invoice, act=detail.act, amount=act_amount
            )

        invoice.amount = total_amount
        invoice.save()

        consultation.invoice = invoice
        consultation.save()

        return redirect("invoices.index")

    return render(request, "invoices/create.html", {"consultations": consultations})


@login_required(login_url="login")
def invoice_show(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    details = InvoiceDetails.objects.filter(invoice=invoice)
    return render(
        request, "invoices/show.html", {"invoice": invoice, "details": details}
    )


@login_required(login_url="login")
def invoice_update(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)

    if request.method == "POST":
        invoice.status = True
        invoice.save()
        return redirect("invoices.show", pk=invoice.pk)

    return render(request, "invoices/edit.html", {"invoice": invoice})


@login_required(login_url="login")
def invoice_pdf(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    details = InvoiceDetails.objects.filter(invoice=invoice)

    consultation = Consultation.objects.filter(invoice=invoice).first()

    template = get_template("invoices/pdf_template.html")
    html = template.render(
        {
            "invoice": invoice,
            "details": details,
            "consultation": consultation,
        }
    )

    buffer = BytesIO()

    pisa_status = pisa.CreatePDF(
        html,
        dest=buffer,
    )

    if pisa_status.err:
        return HttpResponse("We had some errors with code %s" % pisa_status.err)

    buffer.seek(0)
    response = HttpResponse(buffer, content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="invoice_{invoice.code}.pdf"'
    )

    return response


# ========================================
# ============= Ordonnance ===============
# ========================================


def generate_order_code():
    last_order = Order.objects.order_by("id").last()
    if not last_order:
        return "ORDER-000001"

    last_code = last_order.code
    code_number = int(last_code.split("-")[-1]) + 1
    return f"ORDER-{code_number:06d}"


def generate_order_detail_code():
    last_detail = OrderDelails.objects.order_by("id").last()
    if not last_detail:
        return "ORDER-DETAIL-000001"

    last_code = last_detail.code
    code_number = int(last_code.split("-")[-1]) + 1
    return f"ORDER-DETAIL-{code_number:06d}"


@login_required(login_url="login")
def order_index(request):
    orders = Order.objects.all()
    return render(request, "orders/index.html", {"orders": orders})


@login_required(login_url="login")
def order_create(request):
    today = timezone.now().date()
    valid_consultations = Consultation.objects.filter(
        order__isnull=True, expiryDate__gte=today
    )

    if request.method == "POST":
        consultation_id = request.POST.get("consultation")
        medicine_id = request.POST.get("medicine")
        dosage = request.POST.get("dosage")

        consultation = get_object_or_404(Consultation, pk=consultation_id)
        medicine = get_object_or_404(Medicine, pk=medicine_id)

        order_code = generate_order_code()

        order = Order.objects.create(code=order_code, date=timezone.now())

        detail_code = generate_order_detail_code()
        OrderDelails.objects.create(
            code=detail_code, dosage=dosage, order=order, medicine=medicine
        )

        consultation.order = order
        consultation.save()

        return redirect("orders.show", pk=order.pk)

    medicines = Medicine.objects.all()
    return render(
        request,
        "orders/create.html",
        {"consultations": valid_consultations, "medicines": medicines},
    )


@login_required(login_url="login")
def order_show(request, pk):
    order = get_object_or_404(Order, pk=pk)
    details = OrderDelails.objects.filter(order=order)
    consultation = Consultation.objects.filter(order=order).first()

    today = timezone.now().date()
    can_edit = consultation and consultation.expiryDate >= today

    return render(
        request,
        "orders/show.html",
        {
            "order": order,
            "details": details,
            "consultation": consultation,
            "can_edit": can_edit,
        },
    )


@login_required(login_url="login")
def order_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    consultation = Consultation.objects.filter(order=order).first()

    today = timezone.now().date()
    if not consultation or consultation.expiryDate < today:
        messages.error(
            request, "This prescription can no longer be edited as it has expired."
        )
        return redirect("orders.show", pk=order.pk)

    if request.method == "POST":
        medicine_id = request.POST.get("medicine")
        dosage = request.POST.get("dosage")

        medicine = get_object_or_404(Medicine, pk=medicine_id)

        detail_code = generate_order_detail_code()
        OrderDelails.objects.create(
            code=detail_code, dosage=dosage, order=order, medicine=medicine
        )

        return redirect("orders.show", pk=order.pk)

    medicines = Medicine.objects.all()
    return render(
        request,
        "orders/edit.html",
        {"order": order, "medicines": medicines, "consultation": consultation},
    )


@login_required(login_url="login")
def order_pdf(request, pk):
    order = get_object_or_404(Order, pk=pk)
    details = OrderDelails.objects.filter(order=order)
    consultation = Consultation.objects.filter(order=order).first()

    template = get_template("orders/pdf_template.html")
    html = template.render(
        {
            "order": order,
            "details": details,
            "consultation": consultation,
        }
    )

    buffer = BytesIO()

    pisa_status = pisa.CreatePDF(
        html,
        dest=buffer,
    )

    if pisa_status.err:
        return HttpResponse("We had some errors with code %s" % pisa_status.err)

    buffer.seek(0)
    response = HttpResponse(buffer, content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="prescription_{order.code}.pdf"'
    )

    return response
