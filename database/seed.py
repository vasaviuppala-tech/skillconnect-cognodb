"""
database/seed.py

Loads the data from data/seed_data.py into CognoDB.

Run this file directly to (re)seed the database:

    python -m database.seed

SAFE TO RUN MULTIPLE TIMES:
Every query uses MERGE instead of CREATE. MERGE means "find this node/
relationship if it already exists, otherwise create it." So running this
script twice does not produce duplicate candidates, skills, etc. — it
just confirms they're already there.

PARAMETERIZED QUERIES:
Every query below uses UNWIND $rows AS row together with $-style
parameters (row.id, row.name, ...). We never build a query by pasting
Python values into a string. The data is always sent separately from
the query text, which is what the assignment requires and is also just
the correct/safe way to use Cypher.
"""

import logging
from database.connection import init_driver, get_driver, close_driver
from data.seed_data import (
    CANDIDATES, SKILLS, PROJECTS, JOBS,
    HAS_SKILL, WORKED_ON, APPLIED_TO, USES, REQUIRES,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------
# NODE LOADING
# ---------------------------------------------------------------------
# Each function below loads one node type. They all follow the same
# shape: UNWIND the list of dicts, MERGE on `id` (so re-running is
# safe), then SET the other properties.

def seed_candidates(driver, candidates):
    query = """
    UNWIND $rows AS row
    MERGE (c:Candidate {id: row.id})
    SET c.name = row.name,
        c.email = row.email,
        c.experience_level = row.experience_level
    """
    driver.execute_query(query, rows=candidates)
    logger.info(f"Seeded {len(candidates)} Candidate nodes.")


def seed_skills(driver, skills):
    query = """
    UNWIND $rows AS row
    MERGE (s:Skill {id: row.id})
    SET s.name = row.name,
        s.category = row.category
    """
    driver.execute_query(query, rows=skills)
    logger.info(f"Seeded {len(skills)} Skill nodes.")


def seed_projects(driver, projects):
    query = """
    UNWIND $rows AS row
    MERGE (p:Project {id: row.id})
    SET p.name = row.name,
        p.description = row.description
    """
    driver.execute_query(query, rows=projects)
    logger.info(f"Seeded {len(projects)} Project nodes.")


def seed_jobs(driver, jobs):
    query = """
    UNWIND $rows AS row
    MERGE (j:Job {id: row.id})
    SET j.title = row.title,
        j.company = row.company,
        j.location = row.location
    """
    driver.execute_query(query, rows=jobs)
    logger.info(f"Seeded {len(jobs)} Job nodes.")


# ---------------------------------------------------------------------
# RELATIONSHIP LOADING
# ---------------------------------------------------------------------
# Same pattern: UNWIND the list, MATCH the two existing nodes by id,
# then MERGE the relationship between them. MERGE on the relationship
# means running this twice won't create a second parallel edge.

def seed_has_skill(driver, rows):
    query = """
    UNWIND $rows AS row
    MATCH (c:Candidate {id: row.from})
    MATCH (s:Skill {id: row.to})
    MERGE (c)-[r:HAS_SKILL]->(s)
    SET r.proficiency = row.proficiency
    """
    driver.execute_query(query, rows=rows)
    logger.info(f"Seeded {len(rows)} HAS_SKILL relationships.")


def seed_worked_on(driver, rows):
    query = """
    UNWIND $rows AS row
    MATCH (c:Candidate {id: row.from})
    MATCH (p:Project {id: row.to})
    MERGE (c)-[r:WORKED_ON]->(p)
    SET r.role = row.role
    """
    driver.execute_query(query, rows=rows)
    logger.info(f"Seeded {len(rows)} WORKED_ON relationships.")


def seed_applied_to(driver, rows):
    query = """
    UNWIND $rows AS row
    MATCH (c:Candidate {id: row.from})
    MATCH (j:Job {id: row.to})
    MERGE (c)-[r:APPLIED_TO]->(j)
    SET r.status = row.status
    """
    driver.execute_query(query, rows=rows)
    logger.info(f"Seeded {len(rows)} APPLIED_TO relationships.")


def seed_uses(driver, rows):
    query = """
    UNWIND $rows AS row
    MATCH (p:Project {id: row.from})
    MATCH (s:Skill {id: row.to})
    MERGE (p)-[r:USES]->(s)
    """
    driver.execute_query(query, rows=rows)
    logger.info(f"Seeded {len(rows)} USES relationships.")


def seed_requires(driver, rows):
    query = """
    UNWIND $rows AS row
    MATCH (j:Job {id: row.from})
    MATCH (s:Skill {id: row.to})
    MERGE (j)-[r:REQUIRES]->(s)
    """
    driver.execute_query(query, rows=rows)
    logger.info(f"Seeded {len(rows)} REQUIRES relationships.")


# ---------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------

def run_seed():
    """Connects to CognoDB and loads all nodes, then all relationships.

    Nodes are loaded first because relationships MATCH on existing nodes —
    if a relationship step ran before its nodes existed, MATCH would find
    nothing and silently skip that row.
    """
    from dotenv import load_dotenv
    load_dotenv()  # reads .env into environment variables

    connected = init_driver()
    if not connected:
        logger.error("Could not connect to CognoDB. Check your .env file and that the instance is running. Aborting seed.")
        return

    driver = get_driver()

    try:
        # Nodes first
        seed_candidates(driver, CANDIDATES)
        seed_skills(driver, SKILLS)
        seed_projects(driver, PROJECTS)
        seed_jobs(driver, JOBS)

        # Relationships second (they depend on nodes existing)
        seed_has_skill(driver, HAS_SKILL)
        seed_worked_on(driver, WORKED_ON)
        seed_applied_to(driver, APPLIED_TO)
        seed_uses(driver, USES)
        seed_requires(driver, REQUIRES)

        logger.info("Seeding complete.")

    except Exception as e:
        logger.error(f"Seeding failed: {e}")

    finally:
        close_driver()


if __name__ == "__main__":
    run_seed()