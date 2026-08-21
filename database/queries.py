"""
database/queries.py

Every Cypher query the application runs, in one place.

RULES FOLLOWED BY EVERY FUNCTION HERE:
1. Every value that comes from outside (a job_id, a candidate_id, ...)
   is passed as a query PARAMETER (the $name syntax), never pasted
   into the query string. This is what "parameterized" means and it's
   what makes these queries safe from Cypher injection.
2. Each function takes `driver` as its first argument (the same driver
   object created in database/connection.py) and returns plain Python
   data (a list of dicts) — never a raw Neo4j object — so app.py can
   just call json on the result directly.
"""

from neo4j.exceptions import Neo4jError


def _run(driver, query, **params):
    """
    Shared helper: run a query with parameters and return a list of
    plain dicts.

    Centralizing this in one place means every query function below
    is just "here is the Cypher, here are the parameters" — the
    driver-calling boilerplate only needs to be written once.
    """
    result = driver.execute_query(query, **params)
    return [record.data() for record in result.records]


# ---------------------------------------------------------------------
# 1. Jobs
# ---------------------------------------------------------------------

def get_all_jobs(driver):
    """List every job. No parameters needed — nothing here comes from
    outside input, so there's nothing to parameterize."""
    query = """
    MATCH (j:Job)
    RETURN j.id AS id, j.title AS title, j.company AS company, j.location AS location
    ORDER BY j.title
    """
    return _run(driver, query)


# ---------------------------------------------------------------------
# 2. Job -> required skills
# ---------------------------------------------------------------------

def get_job_skills(driver, job_id):
    """Skills a specific job requires. $job_id is a parameter, not a
    string pasted into the query."""
    query = """
    MATCH (j:Job {id: $job_id})-[:REQUIRES]->(s:Skill)
    RETURN s.id AS id, s.name AS name, s.category AS category
    ORDER BY s.name
    """
    return _run(driver, query, job_id=job_id)


# ---------------------------------------------------------------------
# 3. Candidate <-> Job matching (the "relationally awkward" query)
# ---------------------------------------------------------------------
#
# WHY THIS ONE IS AWKWARD IN A RELATIONAL DATABASE:
#
# The question is: "for this job, which candidates share the most
# required skills, and how many?" In a relational schema this needs:
#   - a candidate_skills bridge table
#   - a job_skills bridge table
#   - joining candidate_skills to job_skills on skill_id, filtered to
#     one job
#   - GROUP BY candidate, COUNT(DISTINCT skill_id)
#   - a second query (or subquery) just to know the job's total
#     required-skill count, to show "3 of 5 skills matched"
# That's already 3+ joins and a subquery for a single ranked list.
# If you then wanted to extend the question one more hop — e.g. "and
# which of THEIR projects used those skills" — you'd add another
# bridge-table join per hop, and the query keeps growing.
#
# In Cypher, the relationship IS the join, so the same question reads
# almost like the English sentence that describes it: find the job's
# required skills, find candidates connected to those same skill
# nodes, count how many are shared.

def get_matching_candidates(driver, job_id):
    """Candidates who have at least one skill this job requires,
    ranked by how many of the required skills they match."""
    query = """
    MATCH (j:Job {id: $job_id})-[:REQUIRES]->(s:Skill)
    WITH j, collect(s) AS required_skills, count(s) AS total_required
    MATCH (c:Candidate)-[:HAS_SKILL]->(rs:Skill)
    WHERE rs IN required_skills
    WITH c, total_required, count(DISTINCT rs) AS matched_count
    RETURN c.id AS id,
           c.name AS name,
           c.experience_level AS experience_level,
           matched_count,
           total_required
    ORDER BY matched_count DESC, c.name ASC
    """
    return _run(driver, query, job_id=job_id)


# ---------------------------------------------------------------------
# 4. Candidate details
# ---------------------------------------------------------------------

def get_candidate_details(driver, candidate_id):
    """Basic info for one candidate. Returns an empty list if the id
    doesn't exist — app.py turns that into a 404, not a crash."""
    query = """
    MATCH (c:Candidate {id: $candidate_id})
    RETURN c.id AS id, c.name AS name, c.email AS email, c.experience_level AS experience_level
    """
    return _run(driver, query, candidate_id=candidate_id)


# ---------------------------------------------------------------------
# 5. Candidate -> skills
# ---------------------------------------------------------------------

def get_candidate_skills(driver, candidate_id):
    query = """
    MATCH (c:Candidate {id: $candidate_id})-[r:HAS_SKILL]->(s:Skill)
    RETURN s.id AS id, s.name AS name, s.category AS category, r.proficiency AS proficiency
    ORDER BY s.name
    """
    return _run(driver, query, candidate_id=candidate_id)


# ---------------------------------------------------------------------
# 6. Candidate -> projects
# ---------------------------------------------------------------------

def get_candidate_projects(driver, candidate_id):
    query = """
    MATCH (c:Candidate {id: $candidate_id})-[r:WORKED_ON]->(p:Project)
    RETURN p.id AS id, p.name AS name, p.description AS description, r.role AS role
    ORDER BY p.name
    """
    return _run(driver, query, candidate_id=candidate_id)


# ---------------------------------------------------------------------
# 7. MULTI-HOP: Candidate -> Project -> Skill <- Job (3 hops)
# ---------------------------------------------------------------------
#
# This answers a question a single skill lookup can't: "which jobs
# could this candidate be a fit for based on skills demonstrated
# through real project work, not just their declared skill list?"
#
# The path has three relationships:
#   Candidate -[:WORKED_ON]-> Project -[:USES]-> Skill <-[:REQUIRES]- Job
#
# For each job reached this way, we also collect *which* skills and
# *which* projects formed the connection, so the UI can show the
# reasoning ("qualifies via: Graph Visualizer -> Cypher"), not just
# a bare list of job titles.

def get_candidate_job_matches_via_projects(driver, candidate_id):
    """The 3-hop traversal: candidate's project work -> skills used
    in those projects -> jobs that require those skills."""
    query = """
    MATCH (c:Candidate {id: $candidate_id})-[:WORKED_ON]->(p:Project)
          -[:USES]->(s:Skill)<-[:REQUIRES]-(j:Job)
    RETURN j.id AS job_id,
           j.title AS job_title,
           j.company AS company,
           j.location AS location,
           collect(DISTINCT s.name) AS matched_via_skills,
           collect(DISTINCT p.name) AS matched_via_projects
    ORDER BY job_title
    """
    return _run(driver, query, candidate_id=candidate_id)