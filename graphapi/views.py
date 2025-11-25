from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.urls import reverse

from graphapi.services.graph_write import (
    create_patient,
    patient_add_symptom,
    patient_add_risk_factor,
    patient_add_visit,
    visit_add_observation,
    visit_add_test,
    symptom_indicates_disease,
    disease_add_treatment,
    test_used_for_diagnosis,
    observation_supports_disease,
)

from graphapi.services.graph_read import (
    list_patients,
    get_patient,
    patient_symptoms,
    patient_risk_factors,
    patient_visits,
    visit_observations,
    visit_tests,
    diseases_for_symptom,
    symptoms_for_disease,
    treatments_for_disease,
    diseases_for_test,
    diseases_for_observation,
    search_graph,
)


# -----------------------
# API ROOT
# -----------------------

def _full(request, name: str) -> str:
    return request.build_absolute_uri(reverse(name))


@api_view(["GET"])
def api_root(request):
    return Response({
        # Patients
        "patients_list": _full(request, "patients_list"),
        "patient_detail": _full(request, "patient_detail"),
        "patient_create": _full(request, "patient_create"),
        "patient_add_symptom": _full(request, "patient_add_symptom"),
        "patient_add_risk_factor": _full(request, "patient_add_risk_factor"),
        "patient_add_visit": _full(request, "patient_add_visit"),
        "patient_symptoms": _full(request, "patient_symptoms"),
        "patient_risk_factors": _full(request, "patient_risk_factors"),
        "patient_visits": _full(request, "patient_visits"),

        # Visit
        "visit_observations": _full(request, "visit_observations"),
        "visit_tests": _full(request, "visit_tests"),
        "visit_add_observation": _full(request, "visit_add_observation"),
        "visit_add_test": _full(request, "visit_add_test"),


        # Symptom / Disease / Treatment
        "symptom_indicates_disease": _full(request, "symptom_indicates_disease"),
        "diseases_for_symptom": _full(request, "diseases_for_symptom"),
        "symptoms_for_disease": _full(request, "symptoms_for_disease"),
        "disease_add_treatment": _full(request, "disease_add_treatment"),
        "treatments_for_disease": _full(request, "treatments_for_disease"),

        # Test / Observation
        "test_used_for_diagnosis": _full(request, "test_used_for_diagnosis"),
        "diseases_for_test": _full(request, "diseases_for_test"),
        "observation_supports_disease": _full(request, "observation_supports_disease"),
        "diseases_for_observation": _full(request, "diseases_for_observation"),

        # Utilitaire
        "search": _full(request, "search"),
        
        
    })


# -----------------------
# PATIENT
# -----------------------

@api_view(["GET"])
def patients_list_view(request):
    return Response(list_patients())


@api_view(["GET"])
def patient_detail_view(request):
    name = request.GET.get("name")
    return Response(get_patient(name))


@api_view(["POST"])
def patient_create_view(request):
    name = request.data["name"]
    age = request.data.get("age")
    gender = request.data.get("gender")
    result = create_patient(name, age=age, gender=gender)
    return Response({"status": "ok", "patient": result})


@api_view(["POST"])
def patient_add_symptom_view(request):
    patient = request.data["patient"]
    symptom = request.data["symptom"]
    severity = request.data.get("severity")
    onset_days = request.data.get("onset_days")
    result = patient_add_symptom(patient, symptom, severity=severity, onset_days=onset_days)
    return Response({"status": "ok", "result": result})


@api_view(["POST"])
def patient_add_risk_factor_view(request):
    patient = request.data["patient"]
    risk_name = request.data["risk_name"]
    category = request.data.get("category")
    result = patient_add_risk_factor(patient, risk_name, category=category)
    return Response({"status": "ok", "result": result})


@api_view(["POST"])
def patient_add_visit_view(request):
    patient = request.data["patient"]
    visit_id = request.data["visit_id"]
    date = request.data.get("date")
    reason = request.data.get("reason")
    result = patient_add_visit(patient, visit_id, date=date, reason=reason)
    return Response({"status": "ok", "result": result})


@api_view(["GET"])
def patient_symptoms_view(request):
    name = request.GET.get("name")
    return Response(patient_symptoms(name))


@api_view(["GET"])
def patient_risk_factors_view(request):
    name = request.GET.get("name")
    return Response(patient_risk_factors(name))


@api_view(["GET"])
def patient_visits_view(request):
    name = request.GET.get("name")
    return Response(patient_visits(name))


# -----------------------
# VISIT
# -----------------------

@api_view(["POST"])
def visit_add_observation_view(request):
    visit_id = request.data["visit_id"]
    name = request.data["name"]
    value = request.data["value"]
    unit = request.data.get("unit")
    time = request.data.get("time")
    result = visit_add_observation(visit_id, name, value, unit=unit, time=time)
    return Response({"status": "ok", "result": result})


@api_view(["POST"])
def visit_add_test_view(request):
    visit_id = request.data["visit_id"]
    test_name = request.data["test_name"]
    test_type = request.data.get("test_type")
    result = visit_add_test(visit_id, test_name, test_type=test_type)
    return Response({"status": "ok", "result": result})


@api_view(["GET"])
def visit_observations_view(request):
    visit_id = request.GET.get("visit_id")
    return Response(visit_observations(visit_id))


@api_view(["GET"])
def visit_tests_view(request):
    visit_id = request.GET.get("visit_id")
    return Response(visit_tests(visit_id))


# -----------------------
# SYMPTOM / DISEASE / TREATMENT
# -----------------------

@api_view(["POST"])
def symptom_indicates_disease_view(request):
    symptom = request.data["symptom"]
    disease = request.data["disease"]
    weight = request.data.get("weight")
    result = symptom_indicates_disease(symptom, disease, weight=weight)
    return Response({"status": "ok", "result": result})


@api_view(["GET"])
def diseases_for_symptom_view(request):
    symptom = request.GET.get("symptom")
    return Response(diseases_for_symptom(symptom))


@api_view(["GET"])
def symptoms_for_disease_view(request):
    disease = request.GET.get("disease")
    return Response(symptoms_for_disease(disease))


@api_view(["POST"])
def disease_add_treatment_view(request):
    disease = request.data["disease"]
    treatment = request.data["treatment"]
    line = request.data.get("line")
    recommended = request.data.get("recommended")
    result = disease_add_treatment(disease, treatment, line=line, recommended=recommended)
    return Response({"status": "ok", "result": result})


@api_view(["GET"])
def treatments_for_disease_view(request):
    disease = request.GET.get("disease")
    return Response(treatments_for_disease(disease))


# -----------------------
# TEST / OBSERVATION
# -----------------------

@api_view(["POST"])
def test_used_for_diagnosis_view(request):
    test_name = request.data["test_name"]
    disease = request.data["disease"]
    result = test_used_for_diagnosis(test_name, disease)
    return Response({"status": "ok", "result": result})


@api_view(["GET"])
def diseases_for_test_view(request):
    test_name = request.GET.get("test_name")
    return Response(diseases_for_test(test_name))


@api_view(["POST"])
def observation_supports_disease_view(request):
    obs_name = request.data["observation"]
    disease = request.data["disease"]
    result = observation_supports_disease(obs_name, disease)
    return Response({"status": "ok", "result": result})


@api_view(["GET"])
def diseases_for_observation_view(request):
    obs_name = request.GET.get("observation")
    return Response(diseases_for_observation(obs_name))


# -----------------------
# SEARCH
# -----------------------

@api_view(["GET"])
def search_view(request):
    term = request.GET.get("term", "")
    return Response(search_graph(term))



