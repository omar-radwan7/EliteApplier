'''
Smart CV Selector for Auto Job Applier
Author: Antigravity (for Omar Radwan)

Selects the most appropriate CV based on job title and description language/content.

CV Mapping:
- German-language jobs (description in German or "Deutsch" required):
    -> Omar_Radwan_CV_DE.pdf or Omar_Radwan_CV_DE2.pdf
- Data-related roles (Data Engineer, Data Scientist, Analytics):
    -> Omar_RadwanCV_Data.pdf
- Cloud-related roles (AWS, DevOps, Cloud):
    -> Omar_RadwanCV_Cloud-1.pdf
- All other English roles:
    -> Omar_RadwanCV_ENG.pdf or Omar_RadwanCV_ENG2.pdf
'''

import os

# ======= CV Paths =======
CV_GERMAN_1   = "/home/oradwan/Desktop/Omar Radwan/Omar_Radwan_CV_DE.pdf"
CV_GERMAN_2   = "/home/oradwan/Documents/Omar_Radwan_CV_DE2.pdf"

CV_DATA       = "/home/oradwan/Downloads/Omar_RadwanCV_Data.pdf"
CV_CLOUD      = "/home/oradwan/Documents/Omar_RadwanCV_Cloud-1.pdf"

CV_ENG_1      = "/home/oradwan/Desktop/Omar Radwan/Omar_RadwanCV_ENG.pdf"
CV_ENG_2      = "/home/oradwan/Documents/Omar_RadwanCV_ENG2.pdf"
CV_ENG_3      = "/home/oradwan/Downloads/Omar_RadwanCV_ENG3.pdf"

# ======= Keyword Lists =======

# German language indicators in job descriptions
GERMAN_LANGUAGE_KEYWORDS = [
    # German words commonly found in German-language job postings
    "wir suchen", "deine aufgaben", "dein profil", "was wir bieten",
    "stellenbeschreibung", "anforderungen", "aufgaben", "kenntnisse",
    "erfahrung", "bewerbung", "voraussetzungen", "teamarbeit",
    "idealerweise", "abgeschlossen", "deutschkenntnisse", "deutsch",
    "vollzeit", "teilzeit", "werkstudent", "praktikum", "unbefristet",
    "mehrjährige", "einschlägige", "eigenverantwortlich", "lösungsorientiert",
    "kommunikationsstärke", "eigeninitiative", "verantwortung", "mitarbeiter",
    "selbstständig", "zusammenarbeit", "ansprechpartner", "weiterentwicklung",
    "stellenangebot", "unternehmen", "entwickler", "softwareentwickler",
    "deutschkenntnisse erforderlich", "german required", "german is required",
    "german language required", "b2 german", "c1 german", "fluent german",
    "german speaker", "german speaking", "auf deutsch", "in deutsch"
]

# Data/Analytics role indicators
DATA_KEYWORDS = [
    "data engineer", "data scientist", "data analyst", "data pipeline",
    "machine learning", "ml engineer", "deep learning", "nlp",
    "analytics engineer", "business intelligence", "bi developer",
    "etl", "spark", "hadoop", "airflow", "databricks", "snowflake",
    "dbt", "kafka", "data warehouse", "big data", "data lake",
    "tableau", "power bi", "looker", "pandas", "numpy", "sklearn",
    "pytorch", "tensorflow", "model training", "model deployment",
    "feature engineering", "a/b testing", "statistical analysis",
    "data modeling", "data architecture"
]

# Cloud/DevOps role indicators
CLOUD_KEYWORDS = [
    "cloud engineer", "devops", "site reliability", "sre",
    "aws", "amazon web services", "azure", "google cloud", "gcp",
    "kubernetes", "k8s", "docker", "terraform", "ansible",
    "infrastructure", "ci/cd", "jenkins", "github actions",
    "cloudformation", "helm", "microservices", "service mesh",
    "monitoring", "observability", "prometheus", "grafana",
    "cloud architect", "platform engineer", "devsecops",
    "cloud developer", "cloud practitioner", "cloud solutions"
]


def _is_german_job(title: str, description: str) -> bool:
    """
    Checks if the job is German-language based on the description content.
    Returns True if the job is clearly in German or explicitly requires German.
    """
    text = (title + " " + description).lower()
    german_hits = sum(1 for kw in GERMAN_LANGUAGE_KEYWORDS if kw in text)
    # If 3+ German keywords found, it's likely a German-language posting
    return german_hits >= 3


def _is_data_job(title: str, description: str) -> bool:
    """
    Checks if the job is data/ML/analytics focused.
    """
    text = (title + " " + description).lower()
    return any(kw in text for kw in DATA_KEYWORDS)


def _is_cloud_job(title: str, description: str) -> bool:
    """
    Checks if the job is cloud/DevOps focused.
    """
    text = (title + " " + description).lower()
    return any(kw in text for kw in CLOUD_KEYWORDS)


def _first_existing(*paths: str) -> str:
    """
    Returns the first path that exists on disk from the provided list.
    Falls back to the last path if none exist.
    """
    for p in paths:
        if os.path.exists(p):
            return p
    return paths[-1]  # Return last as fallback even if missing


def select_resume(title: str, description: str) -> str:
    """
    Smart CV selector: picks the best resume for the job.

    Priority order:
    1. German-language job  -> German CV
    2. Data/ML/Analytics    -> Data CV
    3. Cloud/DevOps         -> Cloud CV
    4. Default              -> English CV

    Returns the absolute path to the selected CV.
    """
    title = title or ""
    description = description or ""

    if _is_german_job(title, description):
        chosen = _first_existing(CV_GERMAN_1, CV_GERMAN_2)
        category = "🇩🇪 German"
    elif _is_data_job(title, description):
        chosen = _first_existing(CV_DATA, CV_ENG_1)
        category = "📊 Data/ML"
    elif _is_cloud_job(title, description):
        chosen = _first_existing(CV_CLOUD, CV_ENG_1)
        category = "☁️ Cloud/DevOps"
    else:
        chosen = _first_existing(CV_ENG_1, CV_ENG_2, CV_ENG_3)
        category = "💻 General Engineering"

    print(f"[Smart CV] Selected [{category}] CV: {os.path.basename(chosen)}")
    return chosen
