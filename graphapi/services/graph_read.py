from graphapi.services.db import get_graph

graph = get_graph()

# ======================================================
#                GLOBAL RETRIEVAL FUNCTIONS
# ======================================================

def all_symptoms():
    q = "MATCH (s:Symptom) RETURN toLower(s.name) AS name"
    return [r["name"] for r in graph.run(q).data()]


def all_diseases():
    q = "MATCH (d:Disease) RETURN toLower(d.name) AS name"
    return [r["name"] for r in graph.run(q).data()]


def all_patients():
    q = "MATCH (p:Patient) RETURN toLower(p.name) AS name"
    return [r["name"] for r in graph.run(q).data()]


def all_tests():
    q = "MATCH (t:Test) RETURN toLower(t.name) AS name"
    return [r["name"] for r in graph.run(q).data()]


def all_observations():
    q = "MATCH (o:Observation) RETURN toLower(o.name) AS name"
    return [r["name"] for r in graph.run(q).data()]


# ======================================================
#                    PATIENT QUERIES
# ======================================================

def list_patients():
    q = "MATCH (p:Patient) RETURN p"
    return graph.run(q).data()


def get_patient(name: str):
    q = """
    MATCH (p:Patient)
    WHERE toLower(p.name) = toLower($name)
    RETURN p
    """
    return graph.run(q, name=name).data()


def patient_symptoms(name: str):
    q = """
    MATCH (p:Patient)
    WHERE toLower(p.name) = toLower($name)
    MATCH (p)-[r:HAS_SYMPTOM]->(s:Symptom)
    RETURN s.name AS symptom, r
    """
    return graph.run(q, name=name).data()


def patient_risk_factors(name: str):
    q = """
    MATCH (p:Patient)
    WHERE toLower(p.name) = toLower($name)
    MATCH (p)-[:HAS_RISK_FACTOR]->(r:RiskFactor)
    RETURN r.name AS risk_factor
    """
    return graph.run(q, name=name).data()


def patient_visits(name: str):
    q = """
    MATCH (p:Patient)
    WHERE toLower(p.name) = toLower($name)
    MATCH (p)-[:HAS_VISIT]->(v:Visit)
    RETURN v.id AS visit_id, v
    """
    return graph.run(q, name=name).data()


# ======================================================
#                   VISIT QUERIES
# ======================================================

def visit_observations(visit_id: str):
    q = """
    MATCH (v:Visit)
    WHERE toLower(v.id) = toLower($id)
    MATCH (v)-[:HAS_OBSERVATION]->(o:Observation)
    RETURN o.name AS observation, o
    """
    return graph.run(q, id=visit_id).data()


def visit_tests(visit_id: str):
    q = """
    MATCH (v:Visit)
    WHERE toLower(v.id) = toLower($id)
    MATCH (v)-[:HAS_TEST]->(t:Test)
    RETURN t.name AS test, t
    """
    return graph.run(q, id=visit_id).data()


# ======================================================
#        SYMPTOM / DISEASE / TREATMENT QUERIES
# ======================================================

def diseases_for_symptom(symptom: str):
    q = """
    MATCH (s:Symptom)
    WHERE toLower(s.name) = toLower($symptom)
    MATCH (s)-[:INDICATES]->(d:Disease)
    RETURN d.name AS disease
    """
    records = graph.run(q, symptom=symptom).data()
    return [r["disease"] for r in records]


def symptoms_for_disease(disease: str):
    q = """
    MATCH (d:Disease)
    WHERE toLower(d.name) = toLower($disease)
    MATCH (s:Symptom)-[:INDICATES]->(d)
    RETURN s.name AS symptom
    """
    records = graph.run(q, disease=disease).data()
    return [r["symptom"] for r in records]


def treatments_for_disease(disease: str):
    q = """
    MATCH (d:Disease)
    WHERE toLower(d.name) = toLower($disease)
    MATCH (d)-[:TREATED_BY]->(t:Treatment)
    RETURN t.name AS treatment
    """
    records = graph.run(q, disease=disease).data()
    return [r["treatment"] for r in records]


def diseases_for_test(test_name: str):
    q = """
    MATCH (t:Test)
    WHERE toLower(t.name) = toLower($name)
    MATCH (t)-[:USED_FOR_DIAGNOSIS_OF]->(d:Disease)
    RETURN d.name AS disease
    """
    records = graph.run(q, name=test_name).data()
    return [r["disease"] for r in records]


def diseases_for_observation(obs_name: str):
    q = """
    MATCH (o:Observation)
    WHERE toLower(o.name) = toLower($name)
    MATCH (o)-[:SUPPORTS]->(d:Disease)
    RETURN d.name AS disease
    """
    records = graph.run(q, name=obs_name).data()
    return [r["disease"] for r in records]


def tests_for_disease(disease: str):
    q = """
    MATCH (d:Disease)
    WHERE toLower(d.name) = toLower($disease)
    MATCH (t:Test)-[:USED_FOR_DIAGNOSIS_OF]->(d)
    RETURN t.name AS test
    """
    records = graph.run(q, disease=disease).data()
    return [r["test"] for r in records]


# ======================================================
#                SEARCH (GENERIC QUERY)
# ======================================================

def search_graph(term: str):
    q = """
    MATCH (n)
    WHERE n.name IS NOT NULL AND toLower(n.name) CONTAINS toLower($term)
    RETURN labels(n) AS labels, n AS node
    """
    return graph.run(q, term=term).data()
