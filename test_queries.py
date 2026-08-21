from dotenv import load_dotenv
from database.connection import init_driver, get_driver, close_driver
from database.queries import (
    get_all_jobs,
    get_job_skills,
    get_matching_candidates,
    get_candidate_details,
    get_candidate_skills,
    get_candidate_projects,
    get_candidate_job_matches_via_projects,
)

load_dotenv()

if not init_driver():
    print("Connection failed")
    raise SystemExit(1)

driver = get_driver()

try:
    print("\n1. ALL JOBS")
    print(get_all_jobs(driver))

    print("\n2. JOB SKILLS")
    print(get_job_skills(driver, "j1"))

    print("\n3. MATCHING CANDIDATES")
    print(get_matching_candidates(driver, "j1"))

    print("\n4. CANDIDATE DETAILS")
    print(get_candidate_details(driver, "c1"))

    print("\n5. CANDIDATE SKILLS")
    print(get_candidate_skills(driver, "c1"))

    print("\n6. CANDIDATE PROJECTS")
    print(get_candidate_projects(driver, "c1"))

    print("\n7. MULTI-HOP PROJECT MATCHES")
    print(get_candidate_job_matches_via_projects(driver, "c1"))

finally:
    close_driver()