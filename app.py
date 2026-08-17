from flask import Flask, request, jsonify, render_template_string
from PyPDF2 import PdfReader
import re

app = Flask(__name__)

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>CareerMatch - Job Matcher</title>

<style>

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: Arial, Helvetica, sans-serif;
    min-height: 100vh;
    color: white;

    background:
        radial-gradient(circle at 10% 10%, #1e3a8a 0, transparent 30%),
        radial-gradient(circle at 90% 90%, #065f46 0, transparent 30%),
        #050816;
}

nav {
    width: 90%;
    max-width: 1100px;
    margin: auto;
    padding: 25px 0;

    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo {
    font-size: 24px;
    font-weight: bold;
}

.logo span {
    display: inline-block;
    padding: 8px 12px;
    margin-right: 8px;
    border-radius: 10px;

    background: linear-gradient(
        135deg,
        #3b82f6,
        #10b981
    );
}

nav a {
    color: #aaa;
    text-decoration: none;
    margin-left: 20px;
}

nav a:hover {
    color: white;
}

.hero {
    text-align: center;
    padding: 80px 20px 60px;
}

.badge {
    display: inline-block;
    padding: 10px 18px;
    margin-bottom: 25px;

    color: #93c5fd;

    border: 1px solid #334155;
    border-radius: 30px;
}

.hero h1 {
    font-size: clamp(45px, 7vw, 78px);
    line-height: 1.05;
    margin-bottom: 25px;
}

.gradient {
    color: transparent;

    background:
        linear-gradient(
            90deg,
            #60a5fa,
            #34d399
        );

    background-clip: text;
    -webkit-background-clip: text;
}

.hero p {
    max-width: 680px;
    margin: auto;

    color: #aab2c5;
    font-size: 18px;
    line-height: 1.7;
}

section {
    width: 90%;
    max-width: 1100px;
    margin: auto;
    padding: 55px 0;
}

.title {
    text-align: center;
    margin-bottom: 35px;
}

.title small {
    color: #60a5fa;
    letter-spacing: 3px;
}

.title h2 {
    font-size: 38px;
    margin: 12px 0;
}

.title p {
    color: #9ca3af;
}

.matcher-box {
    max-width: 850px;
    margin: auto;

    padding: 30px;

    border: 1px solid #293548;
    border-radius: 22px;

    background: rgba(255, 255, 255, 0.06);
    backdrop-filter: blur(15px);
}

.upload-area {
    text-align: center;

    padding: 45px 20px;

    border: 2px dashed #475569;
    border-radius: 18px;

    transition: 0.3s;
}

.upload-area:hover,
.upload-area.active {
    border-color: #34d399;
    background: rgba(52, 211, 153, 0.06);
}

.upload-icon {
    font-size: 50px;
    margin-bottom: 15px;
}

.upload-area p {
    color: #94a3b8;
    margin: 12px 0 20px;
}

input[type="file"] {
    display: none;
}

.button {
    border: none;

    padding: 14px 25px;

    border-radius: 10px;

    color: white;
    font-weight: bold;

    cursor: pointer;

    background:
        linear-gradient(
            135deg,
            #2563eb,
            #10b981
        );

    transition: 0.3s;
}

.button:hover {
    transform: translateY(-3px);

    box-shadow:
        0 10px 30px rgba(16, 185, 129, 0.25);
}

.button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

#fileName {
    color: #6ee7b7;
    margin-top: 18px;
}

textarea {
    width: 100%;

    min-height: 220px;

    margin-top: 25px;
    padding: 18px;

    resize: vertical;

    color: white;

    background: #0b1220;

    border: 1px solid #334155;
    border-radius: 12px;

    outline: none;

    font-family: Arial, Helvetica, sans-serif;
    font-size: 15px;
    line-height: 1.6;
}

textarea:focus {
    border-color: #3b82f6;
}

.analyze {
    width: 100%;
    margin-top: 20px;
    font-size: 16px;
}

#results {
    display: none;
}

.cards {
    display: grid;

    grid-template-columns: 1fr 1fr;

    gap: 20px;
}

.card {
    padding: 30px;

    border: 1px solid #293548;
    border-radius: 20px;

    background: rgba(255, 255, 255, 0.06);
}

.score-card {
    text-align: center;
}

.score-circle {
    width: 180px;
    height: 180px;

    margin: auto auto 20px;

    border-radius: 50%;

    display: flex;
    justify-content: center;
    align-items: center;

    background:
        radial-gradient(
            circle,
            #08101f 58%,
            transparent 60%
        ),
        conic-gradient(
            #3b82f6,
            #34d399,
            #3b82f6
        );
}

.score {
    font-size: 45px;
    font-weight: bold;
}

.muted {
    color: #9ca3af;
}

.stats {
    display: grid;

    grid-template-columns:
        repeat(3, 1fr);

    align-items: center;

    text-align: center;

    gap: 15px;
}

.stat-number {
    display: block;

    font-size: 35px;

    font-weight: bold;

    color: #60a5fa;

    margin-bottom: 8px;
}

.skill-list {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}

.skill {
    padding: 8px 14px;

    border-radius: 30px;

    color: #86efac;

    border: 1px solid #166534;

    background:
        rgba(34, 197, 94, 0.1);
}

.missing-skill {
    padding: 8px 14px;

    border-radius: 30px;

    color: #fda4af;

    border: 1px solid #9f1239;

    background:
        rgba(244, 63, 94, 0.1);
}

.suggestions {
    grid-column: span 2;
}

.suggestions li {
    margin: 12px 0;

    color: #c1c8d5;

    line-height: 1.5;
}

.features {
    display: grid;

    grid-template-columns:
        repeat(4, 1fr);

    gap: 20px;
}

.feature {
    padding: 25px;

    border: 1px solid #293548;

    border-radius: 18px;

    background:
        rgba(255, 255, 255, 0.05);

    transition: 0.3s;
}

.feature:hover {
    transform: translateY(-7px);

    border-color: #10b981;
}

.feature-icon {
    font-size: 35px;
    margin-bottom: 15px;
}

.feature p {
    color: #9ca3af;

    line-height: 1.5;

    margin-top: 10px;
}

footer {
    text-align: center;

    color: #71798c;

    padding: 30px;

    border-top: 1px solid #202638;
}

@media (max-width: 800px) {

    .cards {
        grid-template-columns: 1fr;
    }

    .suggestions {
        grid-column: span 1;
    }

    .features {
        grid-template-columns: 1fr 1fr;
    }
}

@media (max-width: 500px) {

    .features {
        grid-template-columns: 1fr;
    }

    .stats {
        grid-template-columns: 1fr;

        gap: 25px;
    }

    nav a {
        display: none;
    }
}

</style>
</head>

<body>

<nav>

    <div class="logo">
        <span>C</span>
        CareerMatch
    </div>

    <div>
        <a href="#matcher">Matcher</a>
        <a href="#features">Features</a>
    </div>

</nav>


<div class="hero">

    <div class="badge">
        🚀 Smart Job Matcher
    </div>

    <h1>
        Find Your
        <br>
        <span class="gradient">
            Job Match.
        </span>
    </h1>

    <p>
        Upload your resume and paste a job description
        to discover how closely your experience matches
        the position.
    </p>

</div>


<section id="matcher">

    <div class="title">

        <small>JOB MATCHER</small>

        <h2>Compare Resume With Job</h2>

        <p>
            Upload your PDF resume and enter the job description.
        </p>

    </div>


    <div class="matcher-box">

        <div id="dropZone" class="upload-area">

            <div class="upload-icon">
                📄
            </div>

            <h3>
                Drop your resume here
            </h3>

            <p>
                or select a PDF file
            </p>

            <input
                type="file"
                id="resume"
                accept=".pdf"
            >

            <button
                class="button"
                id="chooseButton"
            >
                Choose PDF
            </button>

            <div id="fileName"></div>

        </div>


        <textarea
            id="jobDescription"
            placeholder="Paste the job description here...

Example:
We are looking for a Python developer with experience in Flask, SQL, AWS, Docker and Git."
        ></textarea>


        <button
            id="analyze"
            class="button analyze"
        >
            Find Match
        </button>

    </div>

</section>


<section id="results">

    <div class="title">

        <small>MATCH RESULTS</small>

        <h2>Your Job Match</h2>

        <p>
            See how your resume compares with the position.
        </p>

    </div>


    <div class="cards">


        <div class="card score-card">

            <div class="score-circle">

                <div>

                    <span
                        id="score"
                        class="score"
                    >
                        0
                    </span>

                    <span>/100</span>

                </div>

            </div>

            <h3 id="rating">
                Match Score
            </h3>

            <p class="muted">
                Resume compatibility
            </p>

        </div>


        <div class="card stats">

            <div>

                <span
                    id="matchedCount"
                    class="stat-number"
                >
                    0
                </span>

                <span class="muted">
                    Matched
                </span>

            </div>


            <div>

                <span
                    id="missingCount"
                    class="stat-number"
                >
                    0
                </span>

                <span class="muted">
                    Missing
                </span>

            </div>


            <div>

                <span
                    id="keywordCount"
                    class="stat-number"
                >
                    0
                </span>

                <span class="muted">
                    Keywords
                </span>

            </div>

        </div>


        <div class="card">

            <h3>
                ✅ Matching Skills
            </h3>

            <br>

            <div
                id="matchedSkills"
                class="skill-list"
            ></div>

        </div>


        <div class="card">

            <h3>
                ⚠️ Missing Skills
            </h3>

            <br>

            <div
                id="missingSkills"
                class="skill-list"
            ></div>

        </div>


        <div class="card suggestions">

            <h3>
                💡 Recommendations
            </h3>

            <br>

            <ul id="suggestions"></ul>

        </div>

    </div>

</section>


<section id="features">

    <div class="title">

        <small>FEATURES</small>

        <h2>What We Compare</h2>

    </div>


    <div class="features">

        <div class="feature">

            <div class="feature-icon">
                🎯
            </div>

            <h3>
                Match Score
            </h3>

            <p>
                Calculate how closely your resume
                matches the job description.
            </p>

        </div>


        <div class="feature">

            <div class="feature-icon">
                🧠
            </div>

            <h3>
                Skill Matching
            </h3>

            <p>
                Find skills that appear in both
                your resume and the job.
            </p>

        </div>


        <div class="feature">

            <div class="feature-icon">
                🔍
            </div>

            <h3>
                Missing Skills
            </h3>

            <p>
                Identify technologies and skills
                mentioned by the employer.
            </p>

        </div>


        <div class="feature">

            <div class="feature-icon">
                💡
            </div>

            <h3>
                Recommendations
            </h3>

            <p>
                Get suggestions for improving
                your job compatibility.
            </p>

        </div>

    </div>

</section>


<footer>

    CareerMatch © 2026

</footer>


<script>

const resumeInput =
    document.getElementById("resume");

const fileName =
    document.getElementById("fileName");

const chooseButton =
    document.getElementById("chooseButton");

const analyzeButton =
    document.getElementById("analyze");

const dropZone =
    document.getElementById("dropZone");

const jobDescription =
    document.getElementById("jobDescription");


chooseButton.addEventListener(
    "click",
    function () {

        resumeInput.click();

    }
);


resumeInput.addEventListener(
    "change",
    function () {

        if (this.files.length > 0) {

            fileName.textContent =
                "Selected: " +
                this.files[0].name;

        }

    }
);


dropZone.addEventListener(
    "dragover",
    function (event) {

        event.preventDefault();

        dropZone.classList.add("active");

    }
);


dropZone.addEventListener(
    "dragleave",
    function () {

        dropZone.classList.remove("active");

    }
);


dropZone.addEventListener(
    "drop",
    function (event) {

        event.preventDefault();

        dropZone.classList.remove("active");

        if (event.dataTransfer.files.length > 0) {

            resumeInput.files =
                event.dataTransfer.files;

            fileName.textContent =
                "Selected: " +
                event.dataTransfer.files[0].name;

        }

    }
);


analyzeButton.addEventListener(
    "click",
    async function () {

        if (!resumeInput.files.length) {

            alert(
                "Please select a PDF resume."
            );

            return;
        }


        const job =
            jobDescription.value.trim();


        if (!job) {

            alert(
                "Please paste a job description."
            );

            return;
        }


        const file =
            resumeInput.files[0];


        if (
            !file.name
                .toLowerCase()
                .endsWith(".pdf")
        ) {

            alert(
                "Only PDF files are supported."
            );

            return;
        }


        const formData =
            new FormData();


        formData.append(
            "resume",
            file
        );


        formData.append(
            "job_description",
            job
        );


        analyzeButton.textContent =
            "Matching...";

        analyzeButton.disabled =
            true;


        try {

            const response =
                await fetch(
                    "/match",
                    {
                        method: "POST",
                        body: formData
                    }
                );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.error ||
                    "Matching failed."
                );

            }


            showResults(data);


        } catch (error) {

            alert(error.message);


        } finally {

            analyzeButton.textContent =
                "Find Match";

            analyzeButton.disabled =
                false;

        }

    }
);


function showResults(data) {

    document.getElementById(
        "results"
    ).style.display = "block";


    document.getElementById(
        "score"
    ).textContent = data.score;


    document.getElementById(
        "rating"
    ).textContent = data.rating;


    document.getElementById(
        "matchedCount"
    ).textContent =
        data.matched_skills.length;


    document.getElementById(
        "missingCount"
    ).textContent =
        data.missing_skills.length;


    document.getElementById(
        "keywordCount"
    ).textContent =
        data.job_keywords.length;


    const matchedContainer =
        document.getElementById(
            "matchedSkills"
        );


    matchedContainer.innerHTML = "";


    if (
        data.matched_skills.length === 0
    ) {

        matchedContainer.innerHTML =
            '<span class="muted">No matching skills found.</span>';

    } else {

        data.matched_skills.forEach(
            function (skill) {

                const span =
                    document.createElement(
                        "span"
                    );

                span.className =
                    "skill";

                span.textContent =
                    skill;

                matchedContainer.appendChild(
                    span
                );

            }
        );

    }


    const missingContainer =
        document.getElementById(
            "missingSkills"
        );


    missingContainer.innerHTML = "";


    if (
        data.missing_skills.length === 0
    ) {

        missingContainer.innerHTML =
            '<span class="muted">No major missing skills.</span>';

    } else {

        data.missing_skills.forEach(
            function (skill) {

                const span =
                    document.createElement(
                        "span"
                    );

                span.className =
                    "missing-skill";

                span.textContent =
                    skill;

                missingContainer.appendChild(
                    span
                );

            }
        );

    }


    const suggestionsContainer =
        document.getElementById(
            "suggestions"
        );


    suggestionsContainer.innerHTML = "";


    data.suggestions.forEach(
        function (item) {

            const li =
                document.createElement(
                    "li"
                );

            li.textContent =
                item;

            suggestionsContainer.appendChild(
                li
            );

        }
    );


    document
        .getElementById("results")
        .scrollIntoView({
            behavior: "smooth"
        });

}

</script>

</body>
</html>
"""


def extract_text(file):

    reader = PdfReader(file)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def get_skills():

    return [
        "python",
        "java",
        "javascript",
        "typescript",
        "html",
        "css",
        "react",
        "angular",
        "vue",
        "node.js",
        "flask",
        "django",
        "fastapi",
        "sql",
        "mysql",
        "postgresql",
        "mongodb",
        "redis",
        "git",
        "github",
        "docker",
        "kubernetes",
        "aws",
        "azure",
        "gcp",
        "linux",
        "c",
        "c++",
        "c#",
        ".net",
        "machine learning",
        "deep learning",
        "data science",
        "tensorflow",
        "pytorch",
        "pandas",
        "numpy",
        "devops",
        "jenkins",
        "terraform",
        "power bi",
        "tableau",
        "excel",
        "figma",
        "rest api",
        "graphql"
    ]


def analyze_match(resume_text, job_text):

    resume_lower = resume_text.lower()

    job_lower = job_text.lower()

    skills = get_skills()


    matched_skills = []

    missing_skills = []

    job_keywords = []


    for skill in skills:

        skill_lower = skill.lower()

        if skill_lower in job_lower:

            job_keywords.append(skill)

            if skill_lower in resume_lower:

                matched_skills.append(skill)

            else:

                missing_skills.append(skill)


    if len(job_keywords) == 0:

        score = 0

    else:

        score = round(
            (
                len(matched_skills)
                /
                len(job_keywords)
            ) * 100
        )


    score = min(score, 100)


    if score >= 80:

        rating = "Excellent Match"

    elif score >= 60:

        rating = "Strong Match"

    elif score >= 40:

        rating = "Moderate Match"

    elif score >= 20:

        rating = "Weak Match"

    else:

        rating = "Low Match"


    suggestions = []


    if missing_skills:

        suggestions.append(
            "If you genuinely have experience with "
            "the missing skills, add them to your resume."
        )


    if len(matched_skills) < 3:

        suggestions.append(
            "Highlight more job-relevant technical "
            "skills in your resume."
        )


    if "experience" in job_lower:

        if not any(
            word in resume_lower
            for word in [
                "experience",
                "employment",
                "internship"
            ]
        ):

            suggestions.append(
                "Add relevant work or internship experience."
            )


    if "project" in job_lower:

        if "project" not in resume_lower:

            suggestions.append(
                "Add projects demonstrating the required skills."
            )


    if "education" in job_lower:

        if not any(
            word in resume_lower
            for word in [
                "education",
                "university",
                "college",
                "degree"
            ]
        ):

            suggestions.append(
                "Include your relevant education details."
            )


    if not suggestions:

        suggestions.append(
            "Your resume contains many relevant keywords. "
            "Tailor your experience descriptions to the job."
        )


    return {

        "score": score,

        "rating": rating,

        "matched_skills":
            matched_skills,

        "missing_skills":
            missing_skills,

        "job_keywords":
            job_keywords,

        "suggestions":
            suggestions
    }


@app.route("/")
def home():

    return render_template_string(HTML)


@app.route("/match", methods=["POST"])
def match():

    if "resume" not in request.files:

        return jsonify({
            "error":
                "No resume uploaded."
        }), 400


    file = request.files["resume"]


    if file.filename == "":

        return jsonify({
            "error":
                "Please select a resume."
        }), 400


    if not file.filename.lower().endswith(".pdf"):

        return jsonify({
            "error":
                "Only PDF files are supported."
        }), 400


    job_description = request.form.get(
        "job_description",
        ""
    ).strip()


    if not job_description:

        return jsonify({
            "error":
                "Job description is required."
        }), 400


    try:

        resume_text =
            extract_text(file)


        if not resume_text.strip():

            return jsonify({
                "error":
                    "Could not extract text from this PDF."
            }), 400


        result = analyze_match(
            resume_text,
            job_description
        )


        return jsonify(result)


    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
