import logging

from flask import Flask, jsonify, render_template

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

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/jobs/<job_id>")
def job_page(job_id):
    driver = get_driver()

    if driver is None:
        return "Database is not connected.", 503

    try:
        jobs = get_all_jobs(driver)
        job = next((item for item in jobs if item["id"] == job_id), None)

        if job is None:
            return "Job not found.", 404

        return render_template("job_details.html", job=job)

    except Exception as e:
        app.logger.error("Failed to load job page: %s", e)
        return "Unable to load job.", 500

@app.route("/candidates/<candidate_id>")
def candidate_page(candidate_id):
    driver = get_driver()

    if driver is None:
        return "Database is not connected.", 503

    try:
        result = get_candidate_details(driver, candidate_id)

        if not result:
            return "Candidate not found.", 404

        return render_template(
            "candidate_details.html",
            candidate=result[0]
        )

    except Exception as e:
        app.logger.error("Failed to load candidate page: %s", e)
        return "Unable to load candidate.", 500







def require_driver():
    driver = get_driver()

    if driver is None:
        return None, (
            jsonify({
                "error": "Database is not connected. Check CognoDB and .env configuration."
            }),
            503,
        )

    return driver, None


@app.route("/api/jobs", methods=["GET"])
def api_jobs():
    driver, error = require_driver()

    if error:
        return error

    try:
        return jsonify(get_all_jobs(driver))
    except Exception as e:
        app.logger.error("Failed to fetch jobs: %s", e)
        return jsonify({"error": "Failed to fetch jobs"}), 500


@app.route("/api/jobs/<job_id>/skills", methods=["GET"])
def api_job_skills(job_id):
    driver, error = require_driver()

    if error:
        return error

    try:
        return jsonify(get_job_skills(driver, job_id))
    except Exception as e:
        app.logger.error("Failed to fetch job skills: %s", e)
        return jsonify({"error": "Failed to fetch job skills"}), 500


@app.route("/api/jobs/<job_id>/matches", methods=["GET"])
def api_job_matches(job_id):
    driver, error = require_driver()

    if error:
        return error

    try:
        return jsonify(get_matching_candidates(driver, job_id))
    except Exception as e:
        app.logger.error("Failed to fetch candidate matches: %s", e)
        return jsonify({"error": "Failed to fetch candidate matches"}), 500


@app.route("/api/candidates/<candidate_id>", methods=["GET"])
def api_candidate_details(candidate_id):
    driver, error = require_driver()

    if error:
        return error

    try:
        result = get_candidate_details(driver, candidate_id)

        if not result:
            return jsonify({"error": "Candidate not found"}), 404

        return jsonify(result[0])
    except Exception as e:
        app.logger.error("Failed to fetch candidate: %s", e)
        return jsonify({"error": "Failed to fetch candidate"}), 500


@app.route("/api/candidates/<candidate_id>/skills", methods=["GET"])
def api_candidate_skills(candidate_id):
    driver, error = require_driver()

    if error:
        return error

    try:
        return jsonify(get_candidate_skills(driver, candidate_id))
    except Exception as e:
        app.logger.error("Failed to fetch candidate skills: %s", e)
        return jsonify({"error": "Failed to fetch candidate skills"}), 500


@app.route("/api/candidates/<candidate_id>/projects", methods=["GET"])
def api_candidate_projects(candidate_id):
    driver, error = require_driver()

    if error:
        return error

    try:
        return jsonify(get_candidate_projects(driver, candidate_id))
    except Exception as e:
        app.logger.error("Failed to fetch candidate projects: %s", e)
        return jsonify({"error": "Failed to fetch candidate projects"}), 500


@app.route("/api/candidates/<candidate_id>/job-matches", methods=["GET"])
def api_candidate_job_matches(candidate_id):
    driver, error = require_driver()

    if error:
        return error

    try:
        return jsonify(
            get_candidate_job_matches_via_projects(driver, candidate_id)
        )
    except Exception as e:
        app.logger.error("Failed to fetch project-based job matches: %s", e)
        return jsonify({"error": "Failed to fetch project-based job matches"}), 500


@app.before_request
def ensure_database_connection():
    if get_driver() is None:
        init_driver()


def shutdown():
    close_driver()


if __name__ == "__main__":
    load_result = init_driver()

    if not load_result:
        app.logger.warning(
            "Starting Flask without a database connection. "
            "API requests will return a database error."
        )

    try:
        app.run(debug=True)
    finally:
        shutdown()