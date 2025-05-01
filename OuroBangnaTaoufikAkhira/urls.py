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
    # ========== GESTION DES ACTES ==========
    path("acts/", views.act_index, name="acts.index"),
    path("acts/<int:pk>/", views.act_show, name="acts.show"),
    path("acts/create/", views.act_create, name="acts.create"),
    path("acts/store/", views.act_store, name="acts.store"),
    path("acts/<int:pk>/edit/", views.act_edit, name="acts.edit"),
    path("acts/<int:pk>/update/", views.act_update, name="acts.update"),
    path("acts/<int:pk>/destroy/", views.act_destroy, name="acts.destroy"),
]
