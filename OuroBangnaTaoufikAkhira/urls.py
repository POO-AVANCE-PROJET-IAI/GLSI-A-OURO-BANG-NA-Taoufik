from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("patients/", views.patient_index, name="patients.index"),
    path("patients/<int:pk>/", views.patient_show, name="patients.show"),
    path("patients/create/", views.patient_create, name="patients.create"),
    path("patients/store/", views.patient_store, name="patients.store"),
    path("patients/<int:pk>/edit/", views.patient_edit, name="patients.edit"),
    path("patients/<int:pk>/update/", views.patient_update, name="patients.update"),
    path("patients/<int:pk>/destroy/", views.patient_destroy, name="patients.destroy"),
]
