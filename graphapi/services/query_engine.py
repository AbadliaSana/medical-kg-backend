import json
from kgbackend.llm_config import client

from graphapi.services.graph_read import (
    all_symptoms,
    all_diseases,
    all_patients,
    all_tests,
    all_observations,
    diseases_for_symptom,
    symptoms_for_disease,
    treatments_for_disease,
    diseases_for_test,
    diseases_for_observation,
    patient_symptoms,
    patient_risk_factors,
    patient_visits,
    visit_observations,
    visit_tests
)


# ======================================================
#                 LLM EXTRACTION (ENTITIES ONLY)
# ======================================================

def analyze_with_llm(question: str) -> dict:
    prompt = """
You are an advanced medical NLP parser used inside a Knowledge-Graph reasoning system.
Your ONLY task is to extract entities EXACTLY as they appear in the user's question.
You MUST NOT answer the question. You MUST NOT guess. You MUST NOT add any extra text.

RETURN STRICT VALID JSON WITH THIS STRUCTURE:

{
  "intent": "",
  "symptoms": [],
  "diseases": [],
  "patients": [],
  "tests": [],
  "observations": [],
  "visits": []
}

============================
       EXTRACTION RULES
============================

• Extract ONLY words that appear in the question.
• Do NOT infer medical meaning.
• Do NOT rewrite, rephrase, pluralize, or correct spelling.
• Do NOT guess entities.
• If an entity is not explicitly in the question, do NOT include it.
• Format MUST remain valid JSON.

============================
       ENTITY DEFINITIONS
============================

symptoms      → medical symptoms in the question
diseases      → disease names in the question
patients      → human names (examples: Omar, John Doe, Jane)
tests         → medical test names in the question
observations  → measurable observations (temperature, oxygen level, etc.)
visits        → visit identifiers (V001, V002, etc.)

============================
       INTENT PLACEHOLDER
============================

Ignore the intent. Leave intent="".
The system will infer the intent automatically.

============================

QUESTION:
""" + question

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.choices[0].message.content

    try:
        data = json.loads(raw)
        data["intent"] = ""  # Always empty → auto inference later
        return data
    except:
        print("\n⚠️ INVALID JSON FROM LLM:\n", raw)
        return {
            "intent": "",
            "symptoms": [],
            "diseases": [],
            "patients": [],
            "tests": [],
            "observations": [],
            "visits": []
        }


# ======================================================
#                INTENT INFERENCE ENGINE (RULES)
# ======================================================

def infer_intent(question: str, analysis: dict) -> str:
    q = question.lower()
    symptoms = analysis["symptoms"]
    diseases = analysis["diseases"]
    patients = analysis["patients"]
    tests = analysis["tests"]
    observations = analysis["observations"]
    visits = analysis["visits"]

    # -----------------------------
    # VISIT-LEVEL (PLUS SPÉCIFIQUE)
    # -----------------------------
    # 1) Observations d'une visite précise
    if "visit" in q and "observation" in q and visits:
        return "observations_of_visit"

    # 2) Tests d'une visite précise
    if "visit" in q and "test" in q and visits:
        return "tests_of_visit"

    # 3) Liste des visites d'un patient
    if "visit" in q and patients:
        return "visits_of_patient"

    # -----------------------------
    # DISEASE <-> SYMPTOMS
    # -----------------------------
    if "symptom" in q and diseases:
        return "symptoms_of_disease"

    if ("indicate" in q or "cause" in q or "possible" in q) and symptoms:
        return "possible_diseases"

    # -----------------------------
    # TRAITEMENTS
    # -----------------------------
    if ("treatment" in q or "treatments" in q) and diseases:
        return "treatments_for_disease"

    # -----------------------------
    # TESTS / OBSERVATIONS D'UNE MALADIE
    # -----------------------------
    if "test" in q and diseases:
        return "tests_for_disease"

    if "observation" in q and diseases:
        return "observations_for_disease"

    # -----------------------------
    # PATIENT-LEVEL
    # -----------------------------
    if patients:
        if "symptom" in q:
            return "symptoms_of_patient"
        if "risk factor" in q:
            return "risk_factors_of_patient"

    # -----------------------------
    # FALLBACKS
    # -----------------------------
    if symptoms:
        return "possible_diseases"

    return ""



# ======================================================
#                GRAPH EXECUTION (Neo4j)
# ======================================================

def execute_graph_queries(analysis: dict) -> dict:
    intent = analysis.get("intent")
    symptoms = analysis["symptoms"]
    diseases = analysis["diseases"]
    patients = analysis["patients"]
    tests = analysis["tests"]
    observations = analysis["observations"]
    visits = analysis["visits"]

    results = {}

    # Symptoms -> Diseases
    if intent == "possible_diseases":
        disease_sets = []
        for s in symptoms:
            items = diseases_for_symptom(s)
            if items:
                disease_sets.append(set(items))
        results["possible_diseases"] = list(set.intersection(*disease_sets)) if disease_sets else []

    # Disease -> Symptoms
    if intent == "symptoms_of_disease":
        out = []
        for d in diseases:
            out.extend(symptoms_for_disease(d))
        results["symptoms"] = out

    # Disease -> Treatments
    if intent == "treatments_for_disease":
        out = []
        for d in diseases:
            out.extend(treatments_for_disease(d))
        results["treatments"] = out

    # Disease -> Tests
    if intent == "tests_for_disease":
        out = []
        for d in diseases:
            out.extend(diseases_for_test(d))
        results["tests"] = out

    # Observation -> Disease
    if intent == "diseases_supported_by_observation" and observations:
        results["diseases"] = diseases_for_observation(observations[0])

    # Test -> Disease
    if intent == "diseases_diagnosed_by_test" and tests:
        results["diseases"] = diseases_for_test(tests[0])

    # Patient → Symptoms
    if intent == "symptoms_of_patient" and patients:
        results["symptoms"] = patient_symptoms(patients[0])

    # Patient → Risk factors
    if intent == "risk_factors_of_patient" and patients:
        results["risk_factors"] = patient_risk_factors(patients[0])

    # Patient → Visits
    if intent == "visits_of_patient" and patients:
        results["visits"] = patient_visits(patients[0])

    # Visit → Observations
    if intent == "observations_of_visit" and visits:
        results["observations"] = visit_observations(visits[0])

    # Visit → Tests
    if intent == "tests_of_visit" and visits:
        results["tests"] = visit_tests(visits[0])

    return results


# ======================================================
#                     REASONING LAYER
# ======================================================

def build_reasoning(question, analysis, graph_results):
    intent = analysis["intent"]

    final = "No matching information found."

    if intent == "possible_diseases":
        final = f"The possible diseases are: {graph_results.get('possible_diseases', [])}"

    elif intent == "symptoms_of_disease":
        final = f"The symptoms of the disease are: {graph_results.get('symptoms', [])}"

    elif intent == "treatments_for_disease":
        final = f"The recommended treatments are: {graph_results.get('treatments', [])}"

    elif intent == "tests_for_disease":
        final = f"The diagnostic tests are: {graph_results.get('tests', [])}"

    elif intent == "symptoms_of_patient":
        final = f"The patient's symptoms are: {graph_results.get('symptoms', [])}"

    elif intent == "risk_factors_of_patient":
        final = f"The patient's risk factors are: {graph_results.get('risk_factors', [])}"

    elif intent == "visits_of_patient":
        final = f"The patient's visits are: {graph_results.get('visits', [])}"

    elif intent == "observations_of_visit":
        final = f"The visit observations are: {graph_results.get('observations', [])}"

    elif intent == "tests_of_visit":
        final = f"The visit tests are: {graph_results.get('tests', [])}"

    reasoning = f"""
Reasoning Summary:
Based ONLY on the knowledge graph results below, provide a short explanation.

GRAPH RESULTS:
{graph_results}

FINAL ANSWER:
{final}
"""

    return reasoning.strip()


# ======================================================
#                     MAIN PIPELINE
# ======================================================

def process_query(question: str) -> dict:
    analysis = analyze_with_llm(question)
    analysis["intent"] = infer_intent(question, analysis)

    graph_results = execute_graph_queries(analysis)
    reasoning = build_reasoning(question, analysis, graph_results)

    return {
        "question": question,
        "analysis": analysis,
        "graph_results": graph_results,
        "reasoning": reasoning
    }
