const jobsContainer = document.getElementById("jobs");
const loading = document.getElementById("loading");
const errorBox = document.getElementById("error");

const jobDetails = document.getElementById("jobDetails");
const selectedJobTitle = document.getElementById("selectedJobTitle");
const selectedJobInfo = document.getElementById("selectedJobInfo");
const jobSkills = document.getElementById("jobSkills");
const candidateMatches = document.getElementById("candidateMatches");

const candidateDetails = document.getElementById("candidateDetails");
const candidateName = document.getElementById("candidateName");
const candidateInfo = document.getElementById("candidateInfo");
const candidateSkills = document.getElementById("candidateSkills");
const candidateProjects = document.getElementById("candidateProjects");
const projectMatches = document.getElementById("projectMatches");


async function fetchJSON(url) {
    const response = await fetch(url);

    if (!response.ok) {
        const data = await response.json().catch(() => ({}));
        throw new Error(data.error || `Request failed: ${response.status}`);
    }

    return response.json();
}


function showError(message) {
    errorBox.textContent = message;
    errorBox.classList.remove("hidden");
}


function hideError() {
    errorBox.classList.add("hidden");
}


async function loadJobs() {
    try {
        hideError();

        const jobs = await fetchJSON("/api/jobs");

        loading.classList.add("hidden");
        jobsContainer.innerHTML = "";

        if (!jobs.length) {
            jobsContainer.innerHTML =
                '<div class="empty">No jobs found.</div>';
            return;
        }

        jobs.forEach(job => {
            const card = document.createElement("div");
            card.className = "job-card";

            card.innerHTML = `
                <h3>${escapeHTML(job.title)}</h3>
                <p><strong>Company:</strong> ${escapeHTML(job.company)}</p>
                <p><strong>Location:</strong> ${escapeHTML(job.location)}</p>
                <button onclick="selectJob('${escapeHTML(job.id)}')">
                    View Job
                </button>
            `;

            jobsContainer.appendChild(card);
        });

    } catch (error) {
        loading.classList.add("hidden");
        showError(error.message);
    }
}


/*
 * Open the selected job on a separate page in the same browser tab.
 */
function selectJob(jobId) {
    window.location.href = `/jobs/${encodeURIComponent(jobId)}`;
}


function renderSkills(skills) {
    if (!skills.length) {
        jobSkills.innerHTML =
            '<div class="empty">No required skills found.</div>';
        return;
    }

    jobSkills.innerHTML = `
        <div class="skill-list">
            ${skills.map(skill => `
                <span class="skill">
                    ${escapeHTML(skill.name)}
                </span>
            `).join("")}
        </div>
    `;
}


function renderCandidateMatches(matches) {
    if (!matches.length) {
        candidateMatches.innerHTML =
            '<div class="empty">No matching candidates found.</div>';
        return;
    }

    candidateMatches.innerHTML = "";

    matches.forEach(candidate => {
        const card = document.createElement("div");
        card.className = "candidate-card";

        card.innerHTML = `
            <h3>${escapeHTML(candidate.name)}</h3>

            <p>
                Experience:
                ${escapeHTML(candidate.experience_level)}
            </p>

            <p class="match-count">
                Matched skills:
                ${candidate.matched_count}
                / ${candidate.total_required}
            </p>

            <button onclick="selectCandidate('${escapeHTML(candidate.id)}')">
                View Candidate
            </button>
        `;

        candidateMatches.appendChild(card);
    });
}


/*
 * Open the selected candidate on a separate page in the same browser tab.
 */
function selectCandidate(candidateId) {
    window.location.href =
        `/candidates/${encodeURIComponent(candidateId)}`;
}


function renderCandidateSkills(skills) {
    if (!skills.length) {
        candidateSkills.innerHTML =
            '<div class="empty">No skills found.</div>';
        return;
    }

    candidateSkills.innerHTML = `
        <div class="skill-list">
            ${skills.map(skill => `
                <span class="skill">
                    ${escapeHTML(skill.name)}
                    (${escapeHTML(skill.proficiency)})
                </span>
            `).join("")}
        </div>
    `;
}


function renderCandidateProjects(projects) {
    if (!projects.length) {
        candidateProjects.innerHTML =
            '<div class="empty">No projects found.</div>';
        return;
    }

    candidateProjects.innerHTML = "";

    projects.forEach(project => {
        const card = document.createElement("div");
        card.className = "candidate-card";

        card.innerHTML = `
            <h3>${escapeHTML(project.name)}</h3>
            <p>${escapeHTML(project.description)}</p>
            <p>
                <strong>Role:</strong>
                ${escapeHTML(project.role)}
            </p>
        `;

        candidateProjects.appendChild(card);
    });
}


function renderProjectMatches(matches) {
    if (!matches.length) {
        projectMatches.innerHTML =
            '<div class="empty">No project-based job matches found.</div>';
        return;
    }

    projectMatches.innerHTML = "";

    matches.forEach(match => {
        const card = document.createElement("div");
        card.className = "candidate-card";

        card.innerHTML = `
            <h3>${escapeHTML(match.job_title)}</h3>

            <p>
                ${escapeHTML(match.company)}
                • ${escapeHTML(match.location)}
            </p>

            <p>
                <strong>Matched through skills:</strong>
                ${match.matched_via_skills
                    .map(skill => escapeHTML(skill))
                    .join(", ")}
            </p>

            <p>
                <strong>Matched through projects:</strong>
                ${match.matched_via_projects
                    .map(project => escapeHTML(project))
                    .join(", ")}
            </p>
        `;

        projectMatches.appendChild(card);
    });
}


function escapeHTML(value) {
    const div = document.createElement("div");
    div.textContent = value ?? "";
    return div.innerHTML;
}


loadJobs();