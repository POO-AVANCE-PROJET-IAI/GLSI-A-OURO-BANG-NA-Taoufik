from django.db import models
from django.utils import timezone
from datetime import timedelta


def get_expiry_date():
    return timezone.now() + timedelta(days=10)


class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = "users"

    def __str__(self):
        return f"{self.username} {self.email} {self.status}"


class Patient(models.Model):
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100, unique=True)
    emergency_number = models.CharField(max_length=100, unique=True)
    adresse = models.CharField(max_length=100)
    job = models.CharField(max_length=100)

    class Meta:
        db_table = "patients"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Invoice(models.Model):
    code = models.CharField(max_length=100, unique=True)
    date = models.DateField()
    amount = models.IntegerField
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    status = models.BooleanField(default=False)

    class Meta:
        db_table = "invoices"

    def __str__(self):
        return f"{self.code} {self.status}"


class ActType(models.Model):
    code = models.CharField(max_length=100, unique=True)
    libelle = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = "acts_types"

    def __str__(self):
        return f"{self.libelle}"


class Act(models.Model):
    code = models.CharField(max_length=100, unique=True)
    libelle = models.CharField(max_length=100, unique=True)
    amount = models.IntegerField()
    act_type = models.ForeignKey(ActType, on_delete=models.PROTECT)

    class Meta:
        db_table = "acts"

    def __str__(self):
        return f"{self.libelle}"


class InvoiceDetails(models.Model):
    code = models.CharField(max_length=100, unique=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT)
    act = models.ForeignKey(Act, on_delete=models.PROTECT)
    amount = models.IntegerField()

    class Meta:
        db_table = "invoices_details"

    def __str__(self):
        return f"{self.act.libelle} {self.amount}"


class Medicine(models.Model):
    code = models.CharField(max_length=100, unique=True)
    libelle = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = "medicines"

    def __str__(self):
        return f"{self.libelle}"


class Order(models.Model):
    code = models.CharField(max_length=100, unique=True)
    date = models.DateField(default=timezone.now)

    class Meta:
        db_table = "orders"

    def __str__(self):
        return f"{self.code} {self.date}"


class OrderDelails(models.Model):
    code = models.CharField(max_length=100, unique=True)
    dosage = models.CharField(max_length=255)
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT)

    class Meta:
        db_table = "orders_details"

    def __str__(self):
        return f"{self.order.code} {self.medicine.libelle}"


class Consultation(models.Model):
    code = models.CharField(max_length=100, unique=True)
    date = models.DateField(default=timezone.now)
    expiryDate = models.DateField(default=get_expiry_date)

    doctor = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="consultation_doctor"
    )
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT)
    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT, null=True)
    order = models.ForeignKey(Order, on_delete=models.PROTECT, null=True)

    class Meta:
        db_table = "consultations"

    def __str__(self):
        return f"{self.date} {self.patient.first_name} {self.doctor.username}"


class ConsultationDetails(models.Model):
    code = models.CharField(max_length=100, unique=True)
    act = models.ForeignKey(Act, on_delete=models.PROTECT)
    consultation = models.ForeignKey(Consultation, on_delete=models.PROTECT)

    class Meta:
        db_table = "consultations_details"

    def __str__(self):
        return f"{self.code}"
