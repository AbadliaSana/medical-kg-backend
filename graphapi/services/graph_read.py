from graphapi.services.db import get_graph

graph = get_graph()


# -------- PATIENT --------

def list_patients():
    q = "MATCH (p:Patient) RETURN p"
    return graph.run(q).data()


def get_patient(name: str):
    q = "MATCH (p:Patient {name:$name}) RETURN p"
    return graph.run(q, name=name).data()


def patient_symptoms(name: str):
    q = """
    MATCH (p:Patient {name:$name})-[r:HAS_SYMPTOM]->(s:Symptom)
    RETURN s, r
    """
    return graph.run(q, name=name).data()


def patient_risk_factors(name: str):
    q = """
    MATCH (p:Patient {name:$name})-[:HAS_RISK_FACTOR]->(r:RiskFactor)
    RETURN r
    """
    return graph.run(q, name=name).data()


def patient_visits(name: str):
    q = """
    MATCH (p:Patient {name:$name})-[:HAS_VISIT]->(v:Visit)
    RETURN v
    """
    return graph.run(q, name=name).data()


# -------- VISIT --------

def visit_observations(visit_id: str):
    q = """
    MATCH (v:Visit {id:$id})-[:HAS_OBSERVATION]->(o:Observation)
    RETURN o
    """
    return graph.run(q, id=visit_id).data()


def visit_tests(visit_id: str):
    q = """
    MATCH (v:Visit {id:$id})-[:HAS_TEST]->(t:Test)
    RETURN t
    """
    return graph.run(q, id=visit_id).data()


# -------- SYMPTOM / DISEASE / TREATMENT --------

def diseases_for_symptom(symptom: str):
    q = """
    MATCH (s:Symptom {name:$symptom})-[:INDICATES]->(d:Disease)
    RETURN d
    """
    return graph.run(q, symptom=symptom).data()


def symptoms_for_disease(disease: str):
    q = """
    MATCH (s:Symptom)-[:INDICATES]->(d:Disease {name:$disease})
    RETURN s
    """
    return graph.run(q, disease=disease).data()


def treatments_for_disease(disease: str):
    q = """
    MATCH (d:Disease {name:$disease})-[:TREATED_BY]->(t:Treatment)
    RETURN t
    """
    return graph.run(q, disease=disease).data()


def diseases_for_test(test_name: str):
    q = """
    MATCH (t:Test {name:$name})-[:USED_FOR_DIAGNOSIS_OF]->(d:Disease)
    RETURN d
    """
    return graph.run(q, name=test_name).data()


def diseases_for_observation(obs_name: str):
    q = """
    MATCH (o:Observation {name:$name})-[:SUPPORTS]->(d:Disease)
    RETURN d
    """
    return graph.run(q, name=obs_name).data()


# -------- SEARCH GENERIQUE --------

def search_graph(term: str):
    q = """
    MATCH (n)
    WHERE n.name IS NOT NULL AND toLower(n.name) CONTAINS toLower($term)
    RETURN labels(n) AS labels, n AS node
    """
    return graph.run(q, term=term).data()
