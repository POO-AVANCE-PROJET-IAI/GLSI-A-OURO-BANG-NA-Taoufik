# Generated by Django 5.2 on 2025-05-01 12:04

import OuroBangnaTaoufikAkhira.models
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ActType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100, unique=True)),
                ('libelle', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'db_table': 'acts_types',
            },
        ),
        migrations.CreateModel(
            name='Consultation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100, unique=True)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('expiryDate', models.DateField(default=OuroBangnaTaoufikAkhira.models.get_expiry_date)),
            ],
            options={
                'db_table': 'consultations',
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100, unique=True)),
                ('date', models.DateField()),
                ('status', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'invoices',
            },
        ),
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100, unique=True)),
                ('libelle', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'db_table': 'medicines',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100, unique=True)),
                ('date', models.DateField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'orders',
            },
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=100)),
                ('first_name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=100, unique=True)),
                ('emergency_number', models.CharField(max_length=100, unique=True)),
                ('adresse', models.CharField(max_length=100)),
                ('job', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'patients',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('status', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='Act',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100, unique=True)),
                ('libelle', models.CharField(max_length=100, unique=True)),
                ('amount', models.IntegerField()),
                ('act_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='OuroBangnaTaoufikAkhira.acttype')),
            ],
            options={
                'db_table': 'acts',
            },
        ),
        migrations.CreateModel(
            name='ConsultationDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100, unique=True)),
                ('act', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='OuroBangnaTaoufikAkhira.act')),
                ('consultation', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='OuroBangnaTaoufikAkhira.consultation')),
            ],
            options={
                'db_table': 'consultations_details',
            },
        ),
        migrations.AddField(
            model_name='consultation',
            name='invoice',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='OuroBangnaTaoufikAkhira.invoice'),
        ),
        migrations.CreateModel(
            name='InvoiceDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100, unique=True)),
                ('amount', models.IntegerField()),
                ('act', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='OuroBangnaTaoufikAkhira.act')),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='OuroBangnaTaoufikAkhira.invoice')),
            ],
            options={
                'db_table': 'invoices_details',
            },
        ),
        migrations.AddField(
            model_name='consultation',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='OuroBangnaTaoufikAkhira.order'),
        ),
        migrations.CreateModel(
            name='OrderDelails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100, unique=True)),
                ('dosage', models.CharField(max_length=255)),
                ('medicine', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='OuroBangnaTaoufikAkhira.medicine')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='OuroBangnaTaoufikAkhira.order')),
            ],
            options={
                'db_table': 'orders_details',
            },
        ),
        migrations.AddField(
            model_name='consultation',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='OuroBangnaTaoufikAkhira.patient'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='OuroBangnaTaoufikAkhira.user'),
        ),
        migrations.AddField(
            model_name='consultation',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='consultation_doctor', to='OuroBangnaTaoufikAkhira.user'),
        ),
    ]
