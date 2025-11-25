from graphapi.services.db import get_graph

graph = get_graph()


def merge_node(label: str, props: dict):
    """
    Crée ou récupère un nœud (MERGE) avec les propriétés données.
    """
    fields = ", ".join([f"{k}: ${k}" for k in props.keys()])
    query = f"MERGE (n:{label} {{ {fields} }}) RETURN n"
    return graph.run(query, **props).data()


# ---------------------------
# PATIENT + RELATIONS
# ---------------------------

def create_patient(name: str, age: int | None = None, gender: str | None = None):
    props = {"name": name}
    if age is not None:
        props["age"] = age
    if gender is not None:
        props["gender"] = gender
    return merge_node("Patient", props)


def patient_add_symptom(
    patient: str,
    symptom: str,
    severity: str | None = None,
    onset_days: int | None = None,
):
    merge_node("Patient", {"name": patient})
    merge_node("Symptom", {"name": symptom})

    query = """
    MATCH (p:Patient {name: $patient})
    MATCH (s:Symptom {name: $symptom})
    MERGE (p)-[r:HAS_SYMPTOM]->(s)
    SET r.severity = $severity,
        r.onset_days = $onset_days
    RETURN p, r, s
    """
    return graph.run(
        query,
        patient=patient,
        symptom=symptom,
        severity=severity,
        onset_days=onset_days,
    ).data()


def patient_add_risk_factor(patient: str, risk_name: str, category: str | None = None):
    props = {"name": risk_name}
    if category is not None:
        props["category"] = category
    merge_node("Patient", {"name": patient})
    merge_node("RiskFactor", props)

    query = """
    MATCH (p:Patient {name: $patient})
    MATCH (r:RiskFactor {name: $risk_name})
    MERGE (p)-[:HAS_RISK_FACTOR]->(r)
    RETURN p, r
    """
    return graph.run(query, patient=patient, risk_name=risk_name).data()


def patient_add_visit(patient: str, visit_id: str, date: str | None = None, reason: str | None = None):
    props = {"id": visit_id}
    if date is not None:
        props["date"] = date
    if reason is not None:
        props["reason"] = reason

    merge_node("Patient", {"name": patient})
    merge_node("Visit", props)

    query = """
    MATCH (p:Patient {name: $patient})
    MATCH (v:Visit {id: $visit_id})
    MERGE (p)-[:HAS_VISIT]->(v)
    RETURN p, v
    """
    return graph.run(query, patient=patient, visit_id=visit_id).data()


# ---------------------------
# VISIT RELATIONS
# ---------------------------

def visit_add_observation(
    visit_id: str,
    name: str,
    value: float | int | str,
    unit: str | None = None,
    time: str | None = None,
):
    props = {"name": name, "value": value}
    if unit is not None:
        props["unit"] = unit
    if time is not None:
        props["time"] = time

    merge_node("Visit", {"id": visit_id})
    merge_node("Observation", props)

    query = """
    MATCH (v:Visit {id: $visit_id})
    MATCH (o:Observation {name: $name})
    MERGE (v)-[:HAS_OBSERVATION]->(o)
    RETURN v, o
    """
    return graph.run(query, visit_id=visit_id, name=name).data()


def visit_add_test(visit_id: str, test_name: str, test_type: str | None = None):
    props = {"name": test_name}
    if test_type is not None:
        props["type"] = test_type

    merge_node("Visit", {"id": visit_id})
    merge_node("Test", props)

    query = """
    MATCH (v:Visit {id: $visit_id})
    MATCH (t:Test {name: $test_name})
    MERGE (v)-[:HAS_TEST]->(t)
    RETURN v, t
    """
    return graph.run(query, visit_id=visit_id, test_name=test_name).data()


# ---------------------------
# SYMPTOM → DISEASE
# ---------------------------

def symptom_indicates_disease(symptom: str, disease: str, weight: float | None = None):
    merge_node("Symptom", {"name": symptom})
    merge_node("Disease", {"name": disease})

    query = """
    MATCH (s:Symptom {name: $symptom})
    MATCH (d:Disease {name: $disease})
    MERGE (s)-[r:INDICATES]->(d)
    SET r.weight = $weight
    RETURN s, r, d
    """
    return graph.run(query, symptom=symptom, disease=disease, weight=weight).data()


# ---------------------------
# DISEASE → TREATMENT
# ---------------------------

def disease_add_treatment(
    disease: str,
    treatment: str,
    line: str | None = None,
    recommended: bool | None = None,
):
    merge_node("Disease", {"name": disease})
    merge_node("Treatment", {"name": treatment})

    query = """
    MATCH (d:Disease {name: $disease})
    MATCH (t:Treatment {name: $treatment})
    MERGE (d)-[r:TREATED_BY]->(t)
    SET r.line = $line,
        r.recommended = $recommended
    RETURN d, r, t
    """
    return graph.run(
        query,
        disease=disease,
        treatment=treatment,
        line=line,
        recommended=recommended,
    ).data()


# ---------------------------
# TEST / OBSERVATION → DISEASE
# ---------------------------

def test_used_for_diagnosis(test_name: str, disease: str):
    merge_node("Test", {"name": test_name})
    merge_node("Disease", {"name": disease})

    query = """
    MATCH (t:Test {name: $test_name})
    MATCH (d:Disease {name: $disease})
    MERGE (t)-[:USED_FOR_DIAGNOSIS_OF]->(d)
    RETURN t, d
    """
    return graph.run(query, test_name=test_name, disease=disease).data()


def observation_supports_disease(observation_name: str, disease: str):
    merge_node("Observation", {"name": observation_name})
    merge_node("Disease", {"name": disease})

    query = """
    MATCH (o:Observation {name: $obs})
    MATCH (d:Disease {name: $disease})
    MERGE (o)-[:SUPPORTS]->(d)
    RETURN o, d
    """
    return graph.run(query, obs=observation_name, disease=disease).data()
