from django.urls import path
from . import views

urlpatterns = [
    # API ROOT
    path("", views.api_root, name="api_root"),

    # Patients
    path("patients/", views.patients_list_view, name="patients_list"),
    path("patients/detail/", views.patient_detail_view, name="patient_detail"),
    path("patients/create/", views.patient_create_view, name="patient_create"),
    path("patients/add_symptom/", views.patient_add_symptom_view, name="patient_add_symptom"),
    path("patients/add_risk_factor/", views.patient_add_risk_factor_view, name="patient_add_risk_factor"),
    path("patients/add_visit/", views.patient_add_visit_view, name="patient_add_visit"),
    path("patients/symptoms/", views.patient_symptoms_view, name="patient_symptoms"),
    path("patients/risk_factors/", views.patient_risk_factors_view, name="patient_risk_factors"),
    path("patients/visits/", views.patient_visits_view, name="patient_visits"),

    # Visit
    path("visits/add_observation/", views.visit_add_observation_view, name="visit_add_observation"),
    path("visits/add_test/", views.visit_add_test_view, name="visit_add_test"),
    path("visits/observations/", views.visit_observations_view, name="visit_observations"),
    path("visits/tests/", views.visit_tests_view, name="visit_tests"),

    # Symptom / Disease / Treatment
    path("symptoms/indicates_disease/", views.symptom_indicates_disease_view, name="symptom_indicates_disease"),
    path("symptoms/diseases/", views.diseases_for_symptom_view, name="diseases_for_symptom"),
    path("diseases/symptoms/", views.symptoms_for_disease_view, name="symptoms_for_disease"),
    path("diseases/add_treatment/", views.disease_add_treatment_view, name="disease_add_treatment"),
    path("diseases/treatments/", views.treatments_for_disease_view, name="treatments_for_disease"),

    # Test / Observation
    path("tests/used_for_diagnosis/", views.test_used_for_diagnosis_view, name="test_used_for_diagnosis"),
    path("tests/diseases/", views.diseases_for_test_view, name="diseases_for_test"),
    path("observations/supports_disease/", views.observation_supports_disease_view, name="observation_supports_disease"),
    path("observations/diseases/", views.diseases_for_observation_view, name="diseases_for_observation"),

    # Search
    path("search/", views.search_view, name="search"),

]
