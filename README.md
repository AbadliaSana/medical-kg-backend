Medical Knowledge Graph + LLM Reasoning Backend
Django · Neo4j AuraDB · Groq LLaMA 3.1 · REST API

Ce projet implémente une API intelligente capable d’interpréter des questions en langage naturel concernant la santé, d’extraire automatiquement les entités médicales pertinentes, de les relier à un Knowledge Graph (Neo4j), puis de produire une raisonnement structuré basé uniquement sur les données réelles du graphe.

Il combine :

🇩 Django REST Framework

🧠 Groq LLaMA 3.1 (extraction + classification d'intent)

🕸 Neo4j AuraDB (Knowledge Graph)

🔍 Cypher queries dynamiques

🤖 LLM Reasoning basé sur les résultats du graphe

📌 Fonctionnalités principales
✔ 1. Extraction automatique d’entités (NLP)

Le LLM détecte automatiquement dans la question :

Symptômes

Maladies

Patients

Tests

Observations

Visites

Le tout sans hallucination, sans guessing, et en respectant EXACTEMENT les données présentes dans Neo4j.

✔ 2. Classification précise des intentions (intents)

Le moteur détecte automatiquement l’objectif de la question :

Intent	Description
possible_diseases	Symptômes → maladies possibles
symptoms_of_disease	Symptômes associés à une maladie
treatments_for_disease	Traitements recommandés
symptoms_of_patient	Symptômes d’un patient
risk_factors_of_patient	Facteurs de risque d’un patient
visits_of_patient	Visites d’un patient
observations_of_visit	Observations d’une visite
tests_of_visit	Tests d’une visite
diseases_supported_by_observation	Observation → maladies
diseases_diagnosed_by_test	Test → maladies
✔ 3. Exécution dynamique dans Neo4j

Le backend interroge automatiquement le Knowledge Graph via Cypher :

Symptômes → maladies

Maladies → traitements

Patients → symptômes, risques, visites

Visites → tests, observations

Tests / Observations → maladies

Les recherches sont insensibles à la casse, robustes et sécurisées.

✔ 4. Raisonnement médical (LLM Reasoning)

Le LLM génère une réponse structurée :

Basée uniquement sur les résultats du graphe

Sans hallucination

Avec explications synthétiques

Avec une conclusion médicale prudente

🧩 Architecture du projet
kgbackend/
│
├── graphapi/
│   ├── services/
│   │   ├── db.py               → connexion Neo4j
│   │   ├── graph_read.py       → requêtes Cypher en lecture
│   │   ├── graph_write.py      → création et mises à jour
│   │   ├── query_engine.py     → extraction, intent, reasoning
│   │
│   ├── urls.py
│   ├── views.py                → endpoints REST
│
├── kgbackend/
│   ├── settings.py
│   ├── urls.py
│   ├── llm_config.py           → client Groq API
│
├── Pipfile / Pipfile.lock
├── .env                        → clés privées (non commit)
└── README.md

🔌 Endpoints REST principaux
🔍 Query Engine (LLM + Neo4j)
POST /api/query/
{
  "question": "What diseases can be indicated by fever and cough?"
}

👤 Patients
GET  /api/patients/
POST /api/patients/create/
POST /api/patients/add_symptom/
GET  /api/patients/symptoms/?name=Omar

🩺 Visits
GET  /api/visits/observations/?visit_id=V001
GET  /api/visits/tests/?visit_id=V001

😷 Diseases / Symptoms
GET /api/symptoms/diseases/?symptom=fever
GET /api/diseases/symptoms/?disease=COVID-19

🗄 Configuration du fichier .env
NEO4J_URI=bolt+s://xxxx.databases.neo4j.io
NEO4J_USER=neo4j
NEO4J_PASSWORD=********
GROQ_API_KEY=***************


⚠ Ne jamais publier ce fichier sur GitHub

🚀 Installation & Exécution
1️⃣ Installer les dépendances
pipenv install
pipenv shell

2️⃣ Lancer le serveur Django
python manage.py runserver

3️⃣ Tester dans Postman / Swagger
http://127.0.0.1:8000/api/query/

🧪 Exemples de questions supportées
✔ Symptômes d’une maladie
{ "question": "What symptoms are associated with Flu?" }

✔ Traitements d’une maladie
{ "question": "What treatments are recommended for COVID-19?" }

✔ Risques d’un patient
{ "question": "What risk factors does Omar have?" }

✔ Tests d’une visite
{ "question": "What tests were performed during Omar's visit V001?" }

✔ Maladies possibles
{ "question": "What diseases can be indicated by fever and fatigue?" }
