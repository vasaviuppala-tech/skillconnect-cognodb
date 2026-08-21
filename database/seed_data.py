"""
data/seed_data.py

This file holds the raw seed data as plain Python lists/dicts.
It does NOT talk to the database — it just describes what data should
exist. database/seed.py reads these lists and writes them into CognoDB.

Keeping data separate from loading logic means:
- you can read/edit the dataset without touching any Cypher
- the seed script (seed.py) stays short and focused on "how to load"

All of this is realistic DEMO/SEED data for a take-home assignment,
not real people or real companies.
"""

# ---------------------------------------------------------------------
# NODES
# ---------------------------------------------------------------------

CANDIDATES = [
    {"id": "c1", "name": "Asha Patel", "email": "asha.patel@example.com", "experience_level": "Mid"},
    {"id": "c2", "name": "Ben Okafor", "email": "ben.okafor@example.com", "experience_level": "Senior"},
    {"id": "c3", "name": "Chen Wei", "email": "chen.wei@example.com", "experience_level": "Junior"},
    {"id": "c4", "name": "Dana Kowalski", "email": "dana.kowalski@example.com", "experience_level": "Senior"},
    {"id": "c5", "name": "Emeka Nwosu", "email": "emeka.nwosu@example.com", "experience_level": "Mid"},
    {"id": "c6", "name": "Fatima Al-Sayed", "email": "fatima.alsayed@example.com", "experience_level": "Junior"},
    {"id": "c7", "name": "Gustavo Reyes", "email": "gustavo.reyes@example.com", "experience_level": "Mid"},
    {"id": "c8", "name": "Hana Kobayashi", "email": "hana.kobayashi@example.com", "experience_level": "Senior"},
]

SKILLS = [
    {"id": "s1", "name": "Python", "category": "Language"},
    {"id": "s2", "name": "JavaScript", "category": "Language"},
    {"id": "s3", "name": "Flask", "category": "Framework"},
    {"id": "s4", "name": "React", "category": "Framework"},
    {"id": "s5", "name": "SQL", "category": "Database"},
    {"id": "s6", "name": "Cypher", "category": "Database"},
    {"id": "s7", "name": "Docker", "category": "DevOps"},
    {"id": "s8", "name": "AWS", "category": "Cloud"},
    {"id": "s9", "name": "REST APIs", "category": "Architecture"},
    {"id": "s10", "name": "Git", "category": "Tooling"},
    {"id": "s11", "name": "Data Modeling", "category": "Database"},
    {"id": "s12", "name": "CSS", "category": "Frontend"},
]

PROJECTS = [
    {"id": "p1", "name": "Inventory Tracker", "description": "Internal tool for tracking warehouse stock levels."},
    {"id": "p2", "name": "Recipe Sharing App", "description": "A community site for sharing and rating recipes."},
    {"id": "p3", "name": "Graph Visualizer", "description": "A tool to visualize graph database query results."},
    {"id": "p4", "name": "Job Board API", "description": "A backend API powering a small job listing site."},
    {"id": "p5", "name": "Expense Splitter", "description": "An app for splitting shared expenses between friends."},
    {"id": "p6", "name": "Portfolio Site", "description": "A personal portfolio and blog built from scratch."},
]

JOBS = [
    {"id": "j1", "title": "Backend Engineer", "company": "Nimbus Systems", "location": "Remote"},
    {"id": "j2", "title": "Full Stack Developer", "company": "Riverbed Labs", "location": "Bengaluru"},
    {"id": "j3", "title": "Data Platform Engineer", "company": "Cobalt Analytics", "location": "Remote"},
    {"id": "j4", "title": "Frontend Engineer", "company": "Riverbed Labs", "location": "Bengaluru"},
    {"id": "j5", "title": "Graph Database Engineer", "company": "Cobalt Analytics", "location": "Remote"},
]

# ---------------------------------------------------------------------
# RELATIONSHIPS
# Each entry references node ids above. "from" and "to" are node ids.
# ---------------------------------------------------------------------

# Candidate -[:HAS_SKILL {proficiency}]-> Skill
HAS_SKILL = [
    {"from": "c1", "to": "s1", "proficiency": "Advanced"},
    {"from": "c1", "to": "s3", "proficiency": "Advanced"},
    {"from": "c1", "to": "s9", "proficiency": "Intermediate"},
    {"from": "c2", "to": "s1", "proficiency": "Advanced"},
    {"from": "c2", "to": "s6", "proficiency": "Advanced"},
    {"from": "c2", "to": "s11", "proficiency": "Advanced"},
    {"from": "c2", "to": "s8", "proficiency": "Intermediate"},
    {"from": "c3", "to": "s2", "proficiency": "Intermediate"},
    {"from": "c3", "to": "s12", "proficiency": "Intermediate"},
    {"from": "c4", "to": "s1", "proficiency": "Advanced"},
    {"from": "c4", "to": "s5", "proficiency": "Advanced"},
    {"from": "c4", "to": "s7", "proficiency": "Intermediate"},
    {"from": "c4", "to": "s8", "proficiency": "Advanced"},
    {"from": "c5", "to": "s2", "proficiency": "Advanced"},
    {"from": "c5", "to": "s4", "proficiency": "Advanced"},
    {"from": "c5", "to": "s12", "proficiency": "Advanced"},
    {"from": "c6", "to": "s1", "proficiency": "Beginner"},
    {"from": "c6", "to": "s9", "proficiency": "Intermediate"},
    {"from": "c7", "to": "s1", "proficiency": "Intermediate"},
    {"from": "c7", "to": "s3", "proficiency": "Intermediate"},
    {"from": "c7", "to": "s6", "proficiency": "Beginner"},
    {"from": "c8", "to": "s1", "proficiency": "Advanced"},
    {"from": "c8", "to": "s6", "proficiency": "Advanced"},
    {"from": "c8", "to": "s11", "proficiency": "Advanced"},
    {"from": "c8", "to": "s7", "proficiency": "Advanced"},
]

# Candidate -[:WORKED_ON {role}]-> Project
WORKED_ON = [
    {"from": "c1", "to": "p1", "role": "Backend Developer"},
    {"from": "c1", "to": "p4", "role": "Backend Developer"},
    {"from": "c2", "to": "p3", "role": "Lead Developer"},
    {"from": "c2", "to": "p4", "role": "Backend Developer"},
    {"from": "c3", "to": "p2", "role": "Frontend Developer"},
    {"from": "c4", "to": "p1", "role": "Data Engineer"},
    {"from": "c4", "to": "p4", "role": "Backend Developer"},
    {"from": "c5", "to": "p2", "role": "Frontend Developer"},
    {"from": "c5", "to": "p6", "role": "Frontend Developer"},
    {"from": "c6", "to": "p5", "role": "Backend Developer"},
    {"from": "c7", "to": "p3", "role": "Backend Developer"},
    {"from": "c8", "to": "p3", "role": "Data Engineer"},
    {"from": "c8", "to": "p1", "role": "Backend Developer"},
]

# Candidate -[:APPLIED_TO {status}]-> Job
APPLIED_TO = [
    {"from": "c1", "to": "j1", "status": "Interviewing"},
    {"from": "c2", "to": "j5", "status": "Interviewing"},
    {"from": "c3", "to": "j4", "status": "Applied"},
    {"from": "c4", "to": "j3", "status": "Offer"},
    {"from": "c5", "to": "j4", "status": "Applied"},
    {"from": "c6", "to": "j1", "status": "Applied"},
    {"from": "c7", "to": "j5", "status": "Applied"},
    {"from": "c8", "to": "j5", "status": "Interviewing"},
]

# Project -[:USES]-> Skill
USES = [
    {"from": "p1", "to": "s1"},
    {"from": "p1", "to": "s5"},
    {"from": "p1", "to": "s7"},
    {"from": "p2", "to": "s2"},
    {"from": "p2", "to": "s4"},
    {"from": "p2", "to": "s12"},
    {"from": "p3", "to": "s1"},
    {"from": "p3", "to": "s6"},
    {"from": "p3", "to": "s11"},
    {"from": "p4", "to": "s1"},
    {"from": "p4", "to": "s3"},
    {"from": "p4", "to": "s9"},
    {"from": "p5", "to": "s1"},
    {"from": "p5", "to": "s3"},
    {"from": "p6", "to": "s2"},
    {"from": "p6", "to": "s12"},
]

# Job -[:REQUIRES]-> Skill
REQUIRES = [
    {"from": "j1", "to": "s1"},
    {"from": "j1", "to": "s3"},
    {"from": "j1", "to": "s9"},
    {"from": "j2", "to": "s1"},
    {"from": "j2", "to": "s2"},
    {"from": "j2", "to": "s4"},
    {"from": "j3", "to": "s1"},
    {"from": "j3", "to": "s5"},
    {"from": "j3", "to": "s8"},
    {"from": "j4", "to": "s2"},
    {"from": "j4", "to": "s4"},
    {"from": "j4", "to": "s12"},
    {"from": "j5", "to": "s1"},
    {"from": "j5", "to": "s6"},
    {"from": "j5", "to": "s11"},
]