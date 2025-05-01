from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
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
]
