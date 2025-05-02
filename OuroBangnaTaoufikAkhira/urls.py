from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    # ========== AUTHENTIFICATION ==========
    path("login/", views.login_view, name="login"),
    path("home/", views.home, name="home"),
    path('logout/', views.logout_view, name='logout'),
    # ========== GESTION DES PATIENTS ==========
    path("patients/", views.patient_index, name="patients.index"),
    path("patients/<int:pk>/", views.patient_show, name="patients.show"),
    path("patients/create/", views.patient_create, name="patients.create"),
    path("patients/store/", views.patient_store, name="patients.store"),
    path("patients/<int:pk>/edit/", views.patient_edit, name="patients.edit"),
    path("patients/<int:pk>/update/", views.patient_update, name="patients.update"),
    path("patients/<int:pk>/destroy/", views.patient_destroy, name="patients.destroy"),
    # ========== GESTION DES TYPES D'ACTES ==========
    path("acttypes/", views.acttype_index, name="acttypes.index"),
    path("acttypes/<int:pk>/", views.acttype_show, name="acttypes.show"),
    path("acttypes/create/", views.acttype_create, name="acttypes.create"),
    path("acttypes/store/", views.acttype_store, name="acttypes.store"),
    path("acttypes/<int:pk>/edit/", views.acttype_edit, name="acttypes.edit"),
    path("acttypes/<int:pk>/update/", views.acttype_update, name="acttypes.update"),
    path("acttypes/<int:pk>/destroy/", views.acttype_destroy, name="acttypes.destroy"),
    # ========== GESTION DES ACTES ==========
    path("acts/", views.act_index, name="acts.index"),
    path("acts/<int:pk>/", views.act_show, name="acts.show"),
    path("acts/create/", views.act_create, name="acts.create"),
    path("acts/store/", views.act_store, name="acts.store"),
    path("acts/<int:pk>/edit/", views.act_edit, name="acts.edit"),
    path("acts/<int:pk>/update/", views.act_update, name="acts.update"),
    path("acts/<int:pk>/destroy/", views.act_destroy, name="acts.destroy"),
    # ========== GESTION DES MEDICAMENTS ==========
    path("medicines/", views.medicine_index, name="medicines.index"),
    path("medicines/<int:pk>/", views.medicine_show, name="medicines.show"),
    path("medicines/create/", views.medicine_create, name="medicines.create"),
    path("medicines/store/", views.medicine_store, name="medicines.store"),
    path("medicines/<int:pk>/edit/", views.medicine_edit, name="medicines.edit"),
    path("medicines/<int:pk>/update/", views.medicine_update, name="medicines.update"),
    path(
        "medicines/<int:pk>/destroy/", views.medicine_destroy, name="medicines.destroy"
    ),
    # ========== GESTION DES CONSULTATIONS ==========
    path('consultations/', views.consultation_index, name='consultations.index'),
    path('consultations/create/', views.consultation_create, name='consultations.create'),
    path('consultations/<int:pk>/', views.consultation_show, name='consultations.show'),
    path('consultations/<int:pk>/update/', views.consultation_update, name='consultations.update'),
]
