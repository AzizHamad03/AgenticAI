# Agentic AI Recruitment System

An AI-powered recruitment backend built with **Django**, **Django REST Framework**, **PostgreSQL**, **CrewAI**, and **OpenAI**.

The project provides a recruitment workflow in which candidate and job data are stored in the system, AI agents screen resumes against job requirements, personalized interview questions are generated, and the resulting outputs can be persisted and retrieved through the API.

> **Project Status:** 🚧 Active Development  
> The project currently includes the core recruitment data models, REST API layer, resume processing, two CrewAI agents, and an HR screening pipeline that supports both raw-input demo mode and database-driven execution.

---

## Overview

The Agentic AI Recruitment System is designed to automate and assist with different stages of the recruitment process.

The current workflow supports:

1. Creating job positions.
2. Registering candidates.
3. Uploading candidate resumes.
4. Extracting resume text from uploaded files.
5. Screening a candidate against a job position using an AI agent.
6. Generating structured screening results.
7. Generating personalized interview questions using a second AI agent.
8. Running the AI pipeline directly from existing database records using only a candidate ID and job position ID.
9. Persisting database-driven pipeline results as `ScreeningResult` and `InterviewQuestionSet` records.
10. Retrieving stored results through REST API endpoints.

The project follows a modular architecture that separates models, serializers, views, services, AI crews, and flow orchestration.

---

## Current Features

The current implementation includes:

- Department management
- Job position management
- Candidate registration
- Resume uploads
- Resume file-type validation
- PDF, DOCX, and TXT resume text extraction
- PostgreSQL database integration
- Django REST Framework serializers
- Custom DRF `APIView` endpoints
- Structured API validation and error handling
- Django Admin integration
- Environment-based configuration
- OpenAI configuration
- CrewAI integration
- Resume Screening AI Agent
- Interview Question Generation AI Agent
- CrewAI HR pipeline orchestration
- Raw-input pipeline demo mode
- Database-driven pipeline mode
- Latest-resume selection for database mode
- Automatic persistence of screening results
- Automatic persistence of interview question sets
- Human-readable pipeline errors
- Atomic persistence of related AI results

---

## REST API

The project currently exposes five REST API endpoints.

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/job-positions/` | Create a new job position |
| `POST` | `/api/candidates/` | Register a new candidate |
| `POST` | `/api/resumes/` | Upload a candidate resume |
| `GET` | `/api/screening-results/<id>/` | Retrieve a screening result |
| `GET` | `/api/interview-question-sets/<id>/` | Retrieve generated interview questions |

All endpoints are implemented using custom Django REST Framework `APIView` classes.

### API Behavior

The API uses standard HTTP response codes:

- `200 OK` — successful retrieval
- `201 Created` — successful resource creation
- `400 Bad Request` — invalid input
- `404 Not Found` — requested resource does not exist

Validation and API output are handled through DRF serializers.

---

## Example API Requests

### Create a Job Position

```http
POST /api/job-positions/
```

Example request body:

```json
{
  "department": 1,
  "title": "Backend Engineer",
  "description": "Build and scale Django REST APIs on PostgreSQL.",
  "required_skills": [
    "Python",
    "Django",
    "PostgreSQL"
  ]
}
```

---

### Register a Candidate

```http
POST /api/candidates/
```

Example request body:

```json
{
  "full_name": "Jane Doe",
  "email": "jane@example.com",
  "phone": "+1-555-0100"
}
```

Candidate emails are unique, and duplicate registrations return a validation error.

---

### Upload a Resume

```http
POST /api/resumes/
Content-Type: multipart/form-data
```

Form fields:

```text
candidate = <candidate_id>
file      = <resume_file>
```

Supported resume formats:

```text
.pdf
.docx
.txt
```

Uploaded files are stored under:

```text
media/resumes/
```

Example using `curl`:

```bash
curl -X POST \
  -F "candidate=1" \
  -F "file=@/path/to/resume.pdf" \
  http://127.0.0.1:8000/api/resumes/
```

---

### Retrieve a Screening Result

```http
GET /api/screening-results/1/
```

A screening result can include:

- Candidate
- Job position
- Match score
- Strengths
- Missing skills
- Recommendation
- Summary
- Raw AI-generated report
- Generation timestamp

Example with `curl`:

```bash
curl http://127.0.0.1:8000/api/screening-results/1/
```

---

### Retrieve Interview Questions

```http
GET /api/interview-question-sets/1/
```

The response can contain:

- Technical questions
- Behavioral questions
- Follow-up questions
- Candidate
- Job position
- Screening result
- Generation timestamp

Example with `curl`:

```bash
curl http://127.0.0.1:8000/api/interview-question-sets/1/
```

---

# AI Agent Architecture

The AI layer currently consists of two specialized CrewAI crews coordinated by `HRPipelineFlow`.

## Resume Screening Agent

The Resume Screening Agent evaluates a candidate's resume against the selected job position.

Inputs include:

- Candidate resume text
- Job title
- Job description
- Required skills

The agent produces a structured screening report containing information such as:

- Match score
- Technical skills
- Soft skills
- Candidate strengths
- Missing skills
- Hiring recommendation
- Screening summary

The screening report is parsed into structured JSON before being passed to the next pipeline step.

---

## Interview Question Generator

The Interview Question Generator runs after resume screening.

It receives:

- Candidate resume
- Job title
- Job description
- Screening report

It produces personalized interview questions grouped into:

- Technical questions
- Behavioral questions
- Follow-up questions

---

## HR Pipeline Flow

The two agents are coordinated by:

```text
core/flows/hr_pipeline/flow.py
```

The flow uses CrewAI Flow concepts including:

- state
- `@start`
- `@listen`
- `kickoff()`

The execution sequence is:

```text
Resume Screening Agent
        |
        v
Structured Screening Report
        |
        v
Interview Question Agent
        |
        v
Structured Interview Questions
        |
        v
Combined Pipeline Result
```

`HRPipelineFlow` supports two execution modes:

1. **Raw-input mode**
2. **Database mode**

---

# Running the HR Pipeline

## Mode 1 — Raw-Input Demo

Raw mode is intended for local demonstration and backward compatibility.

The caller provides the resume text and job information directly.

Example:

```python
flow = HRPipelineFlow()

result = flow.kickoff(
    candidate_resume=resume_text,
    job_title="Backend Engineer",
    job_description="Build and maintain scalable backend APIs.",
    required_skills=[
        "Python",
        "Django",
        "PostgreSQL",
        "REST APIs",
        "Git"
    ],
)
```

The project includes:

```text
run_pipeline.py
```

Run it with:

```bash
python run_pipeline.py
```

### Raw Mode Behavior

Raw mode:

- Reads the demo resume
- Extracts its text
- Runs the Resume Screening Agent
- Runs the Interview Question Generator
- Prints the combined output
- Does **not** create `ScreeningResult` records
- Does **not** create `InterviewQuestionSet` records

This preserves the original no-database demonstration behavior.

---

# Database-Driven Pipeline — HRMS-201

HRMS-201 adds a second execution mode that runs entirely from data already stored in the application database.

Instead of supplying resume text, a job description, and skills manually, the caller supplies only:

- `candidate_id`
- `job_position_id`

Example:

```python
flow = HRPipelineFlow()

result = flow.kickoff(
    candidate_id=1,
    job_position_id=2,
)
```

Providing both IDs activates **database mode**.

Both IDs must be supplied together.

For example, this is invalid:

```python
flow.kickoff(
    candidate_id=1,
)
```

and produces a clear error because the job position ID is missing.

---

## What Database Mode Loads

Given:

```text
candidate_id = 1
job_position_id = 2
```

the pipeline automatically loads:

### From the Candidate

- Candidate database record
- Candidate's most recently uploaded resume

### From the Resume

- Resume file
- Extracted plain-text resume content

### From the Job Position

- Job title
- Job description
- Required skills

The caller does not need to provide:

- Resume text
- Job title
- Job description
- Required skills
- API secrets

---

## Latest Resume Selection

A candidate may have multiple uploaded resumes.

Database mode always selects the newest one using the resume's `uploaded_at` field.

Conceptually:

```python
Resume.objects.filter(
    candidate=candidate
).order_by(
    "-uploaded_at"
).first()
```

For example:

```text
Resume A — August 1
Resume B — August 10
Resume C — August 15
```

The pipeline uses:

```text
Resume C
```

---

## Resume Text Extraction

Resume parsing is handled by:

```text
core/services/resume_parser.py
```

The parser supports:

- PDF
- DOCX
- TXT

It can process both:

- regular filesystem paths used by the raw demo
- Django `FieldFile` objects loaded from a `Resume` database record

This allows both pipeline modes to reuse the same resume extraction logic.

---

## Database Mode Execution

The database-driven sequence is:

```text
candidate_id + job_position_id
              |
              v
       Load Candidate
              |
              v
       Load JobPosition
              |
              v
 Find Candidate's Latest Resume
              |
              v
     Extract Resume Text
              |
              v
    Resume Screening Agent
              |
              v
      Screening Report
              |
              v
 Interview Question Generator
              |
              v
     Interview Questions
              |
              v
      Save ScreeningResult
              |
              v
   Save InterviewQuestionSet
              |
              v
       Return Result + IDs
```

---

## Running Database Mode

A separate script is provided:

```text
run_pipeline_db.py
```

Run it using:

```bash
python run_pipeline_db.py <candidate_id> <job_position_id>
```

Example:

```bash
python run_pipeline_db.py 1 2
```

where:

```text
1 = candidate ID
2 = job position ID
```

Before running the command, the database must already contain:

1. A valid candidate
2. At least one uploaded resume for that candidate
3. A valid job position

---

## Successful Database-Mode Output

A successful execution returns the normal agent outputs plus the IDs of the persisted records.

Example:

```json
{
  "screening_report": {
    "match_score": 84,
    "technical_skills": [
      "Python",
      "Django",
      "PostgreSQL"
    ],
    "soft_skills": [
      "Communication",
      "Teamwork"
    ],
    "strengths": [
      "Strong Python background",
      "Relevant backend development experience"
    ],
    "missing_skills": [
      "Limited evidence of production deployment"
    ],
    "hiring_recommendation": "proceed",
    "summary": "The candidate demonstrates strong alignment with the position."
  },
  "interview_questions": {
    "technical_questions": [
      "Example technical question"
    ],
    "behavioral_questions": [
      "Example behavioral question"
    ],
    "follow_up_questions": [
      "Example follow-up question"
    ]
  },
  "database_records": {
    "screening_result_id": 5,
    "interview_question_set_id": 3
  }
}
```

The exact AI-generated content varies between runs.

---

## Persisted Results

Database mode creates two records after both AI agents finish successfully.

### ScreeningResult

The screening output is stored as a `ScreeningResult` linked to:

- Candidate
- Job position

Stored information includes:

- Match score
- Strengths
- Missing skills
- Recommendation
- Summary
- Complete raw screening report

### InterviewQuestionSet

The generated questions are stored as an `InterviewQuestionSet` linked to:

- Candidate
- Job position
- Screening result

Stored information includes:

- Technical questions
- Behavioral questions
- Follow-up questions

Both records are created in a database transaction so they are persisted together.

---

## Reading Persisted Results

If database mode returns:

```json
{
  "database_records": {
    "screening_result_id": 5,
    "interview_question_set_id": 3
  }
}
```

retrieve the screening result through:

```http
GET /api/screening-results/5/
```

or:

```bash
curl http://127.0.0.1:8000/api/screening-results/5/
```

Retrieve the interview questions through:

```http
GET /api/interview-question-sets/3/
```

or:

```bash
curl http://127.0.0.1:8000/api/interview-question-sets/3/
```

The same GET endpoints can also be opened in a browser while the Django development server is running.

---

## Database-Mode Error Handling

Database mode raises human-readable errors for common invalid conditions.

### Candidate Does Not Exist

Example:

```text
Pipeline error: Candidate with id 100 was not found.
```

### Job Position Does Not Exist

Example:

```text
Pipeline error: Job position with id 100 was not found.
```

### Candidate Has No Resume

Example:

```text
Pipeline error: Candidate with id 4 has no resume on file.
```

### Only One ID Is Provided

Example:

```text
Pipeline error: Database mode requires both candidate_id and job_position_id.
```

### Resume Cannot Be Read

The pipeline also reports a readable error when the newest resume cannot be processed or contains no extractable text.

---

## Django ORM and Async Flow Steps

Some CrewAI flow steps are asynchronous.

The project's Django ORM calls are intentionally kept outside those asynchronous agent steps.

Database loading happens synchronously before the asynchronous CrewAI flow begins:

```text
_load_database_inputs()
        |
        v
super().kickoff()
```

Persistence happens synchronously after the CrewAI flow finishes:

```text
super().kickoff()
        |
        v
_persist_database_results()
```

Overall:

```text
kickoff()
   |
   +-- Database mode:
   |      Load database inputs
   |
   +-- Run CrewAI flow
   |      |
   |      +-- async Resume Screening Agent
   |      |
   |      +-- async Interview Question Agent
   |
   +-- Database mode:
          Persist results
```

This keeps normal synchronous Django ORM operations out of the asynchronous flow listeners and avoids `SynchronousOnlyOperation` issues.

---

## Service Layer

Database-related responsibilities are separated into reusable services.

### Resume Parser

```text
core/services/resume_parser.py
```

Responsible for:

- PDF extraction
- DOCX extraction
- TXT extraction
- Filesystem path handling
- Django uploaded-file handling

### Screening Service

```text
core/services/screening_service.py
```

Responsible for converting the screening agent's structured output into a persisted `ScreeningResult`.

### Interview Service

```text
core/services/interview_service.py
```

Responsible for converting the interview agent's structured output into a persisted `InterviewQuestionSet`.

---

## Tech Stack

### Backend

- Python
- Django 4.2
- Django REST Framework

### Database

- PostgreSQL

### AI and Agent Orchestration

- CrewAI
- OpenAI API
- CrewAI Tools

### Document Processing

- PDFPlumber
- python-docx

### Configuration

- python-decouple

---

## Project Structure

```text
AgenticAI/
│
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── core/
│   ├── migrations/
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── candidate.py
│   │   ├── department.py
│   │   ├── interview_question_set.py
│   │   ├── job_position.py
│   │   ├── resume.py
│   │   └── screening_result.py
│   │
│   ├── serializers/
│   │   ├── __init__.py
│   │   └── hr_serializers.py
│   │
│   ├── views/
│   │   ├── __init__.py
│   │   ├── candidate_create.py
│   │   ├── interview_question_set_detail.py
│   │   ├── job_position_create.py
│   │   ├── resume_upload.py
│   │   └── screening_result_detail.py
│   │
│   ├── crews/
│   │   ├── resume_screening/
│   │   │   ├── config/
│   │   │   │   ├── agents.yaml
│   │   │   │   └── tasks.yaml
│   │   │   └── crew.py
│   │   │
│   │   └── interview_question/
│   │       ├── config/
│   │       │   ├── agents.yaml
│   │       │   └── tasks.yaml
│   │       └── crew.py
│   │
│   ├── flows/
│   │   └── hr_pipeline/
│   │       ├── __init__.py
│   │       ├── flow.py
│   │       └── schema.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── interview_service.py
│   │   ├── resume_parser.py
│   │   └── screening_service.py
│   │
│   ├── tools/
│   │   ├── __init__.py
│   │   └── main_llm.py
│   │
│   ├── admin.py
│   ├── apps.py
│   ├── urls.py
│   └── utils.py
│
├── media/
│   └── resumes/
│
├── .env.example
├── .gitignore
├── manage.py
├── requirements.txt
├── run_pipeline.py
├── run_pipeline_db.py
└── readme.md
```

The structure will continue to expand as additional workflow features, authentication, tests, and APIs are introduced.

---

# Data Models

## Department

Represents a department within the organization.

---

## JobPosition

Represents an available position and stores information such as:

- Job title
- Department
- Description
- Required skills

Database mode reads the title, description, and required skills directly from this model.

---

## Candidate

Stores candidate information including:

- Full name
- Email
- Phone number
- Creation date

---

## Resume

Associates an uploaded resume file with a candidate.

A candidate may have multiple resume records.

Database mode selects the newest resume according to `uploaded_at`.

---

## ScreeningResult

Stores the structured result of evaluating a candidate against a job position.

The model supports information such as:

- Match score
- Strengths
- Missing skills
- Recommendation
- Summary
- Raw screening report

In database mode this record is automatically created after successful agent execution.

---

## InterviewQuestionSet

Stores interview questions associated with:

- Candidate
- Job position
- Screening result

Question categories include:

- Technical questions
- Behavioral questions
- Follow-up questions

In database mode this record is automatically created after the screening result.

---

# Getting Started

## 1. Clone the Repository

```bash
git clone <repository-url>
cd AgenticAI
```

---

## 2. Create a Virtual Environment

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file in the project root.

You can use `.env.example` as a starting point:

```bash
cp .env.example .env
```

Configure the required environment variables:

```env
# Django
SECRET_KEY='your-secret-key'
DEBUG=True
ALLOWED_HOSTS='*'

# PostgreSQL
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_USER=your-database-user
DATABASE_PASSWORD=your-database-password
DATABASE_NAME=your-database-name
DATABASE_SCHEMA=public

# OpenAI
OPENAI_API_KEY='your-openai-api-key'
OPENAI_MODEL='gpt-4o-mini'
OPENAI_MAX_RETRIES=3
OPENAI_DEFAULT_TEMPERATURE=0.3
```

> Never commit your real `.env` file, database credentials, secret keys, or API keys to version control.

---

# Database Setup

Make sure PostgreSQL is installed and running.

Create the PostgreSQL database specified in your `.env` file and apply migrations:

```bash
python manage.py migrate
```

When model definitions are intentionally changed during future development, create migrations first with:

```bash
python manage.py makemigrations
```

HRMS-201 itself does not require new model migrations because it uses the existing models.

---

# Run the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

The API will normally be available at:

```text
http://127.0.0.1:8000/
```

Django Admin is available at:

```text
http://127.0.0.1:8000/admin/
```

---

# Create an Admin User

Create a Django superuser with:

```bash
python manage.py createsuperuser
```

Then start the server and visit:

```text
http://127.0.0.1:8000/admin/
```

The Django Admin interface can be used to manage departments, job positions, candidates, resumes, screening results, and interview question sets.

---

# Development Checks

Run Django's built-in system checks with:

```bash
python manage.py check
```

A correctly configured project should return:

```text
System check identified no issues (0 silenced).
```

---

# Testing HRMS-201 Manually

A useful manual acceptance-test sequence is described below.

## Test 1 — Successful Database Run

Make sure the database contains:

- a candidate
- at least one resume for that candidate
- a job position

Then run:

```bash
python run_pipeline_db.py 1 2
```

Expected behavior:

- latest resume is loaded
- job data is loaded
- both agents run
- `ScreeningResult` is created
- `InterviewQuestionSet` is created
- both generated record IDs are printed

---

## Test 2 — Candidate With No Resume

Create a candidate without uploading a resume.

Then run:

```bash
python run_pipeline_db.py <candidate_id> <job_position_id>
```

Expected behavior:

```text
Pipeline error: Candidate with id <candidate_id> has no resume on file.
```

The user should receive a readable message instead of a raw traceback.

---

## Test 3 — Raw Demo Still Works

Run:

```bash
python run_pipeline.py
```

Expected behavior:

- resume is read from the raw demo input
- screening report is generated
- interview questions are generated
- result is printed
- no `ScreeningResult` is written by the flow
- no `InterviewQuestionSet` is written by the flow

---

## Test 4 — Read Persisted Results

After a successful database run, use the returned IDs.

For example:

```text
screening_result_id = 5
interview_question_set_id = 3
```

Open:

```text
http://127.0.0.1:8000/api/screening-results/5/
```

and:

```text
http://127.0.0.1:8000/api/interview-question-sets/3/
```

or retrieve them using Postman or `curl`.

---

# Roadmap

## Completed

- [x] Initial Django project setup
- [x] PostgreSQL configuration
- [x] Core recruitment models
- [x] Django Admin registration
- [x] DRF serializers
- [x] Job Position creation API
- [x] Candidate registration API
- [x] Resume upload API
- [x] Resume extension validation
- [x] Screening Result retrieval API
- [x] Interview Question Set retrieval API
- [x] API validation and error handling
- [x] Media storage configuration
- [x] Resume text extraction
- [x] Resume Screening AI Agent
- [x] Interview Question Generation Agent
- [x] CrewAI HR pipeline orchestration
- [x] Structured AI output parsing
- [x] Raw-input pipeline demo
- [x] Database-driven pipeline using candidate and job IDs
- [x] Latest candidate resume lookup
- [x] Automatic `ScreeningResult` persistence
- [x] Automatic `InterviewQuestionSet` persistence
- [x] Human-readable database-mode errors
- [x] Backward compatibility for raw pipeline mode

## Planned

- [ ] Dedicated REST endpoint for triggering pipeline execution
- [ ] Candidate/job matching workflow
- [ ] Candidate ranking
- [ ] Authentication and authorization
- [ ] Extended API documentation
- [ ] Automated unit and API tests
- [ ] Pipeline integration tests
- [ ] Logging and monitoring improvements
- [ ] Frontend integration
- [ ] Deployment configuration

The roadmap will continue to evolve as development progresses.

---

# Future Vision

The long-term goal is to develop this project into a multi-agent recruitment platform where specialized AI agents collaborate throughout the hiring lifecycle.

Possible future capabilities include:

- Intelligent resume analysis
- Candidate ranking
- Skill-gap detection
- Job-to-candidate matching
- Personalized interview generation
- Interview evaluation
- Candidate summaries
- Recruitment recommendations
- Automated recruitment workflows
- Human review and approval steps
- Recruitment analytics

The objective is not simply to integrate an LLM, but to build structured, maintainable **agentic workflows** that can support real recruitment processes.

---

# Security

Sensitive information such as:

- OpenAI API keys
- Database passwords
- Django secret keys
- Other service credentials

should always be stored in environment variables.

The `.env` file should remain excluded from version control through `.gitignore`.

Resume content and job text do not need to be passed by the caller when database mode is used because the pipeline loads them directly from the application's stored data.

Additional authentication, authorization, and production security measures should be introduced before production deployment.

---

# Contributing

The project is currently under active development.

Contribution guidelines, coding conventions, testing requirements, and development workflows may be introduced as the codebase matures.

---

# License

A license has not yet been selected for this project.

---

# Development Status

**Current Stage:** Active Development — Core Backend, AI Agents & Database-Driven Pipeline

The project currently provides:

- the foundational recruitment data layer
- REST API functionality
- resume parsing
- AI-based resume screening
- AI-generated interview questions
- CrewAI flow orchestration
- database-driven pipeline execution
- persistent AI screening and interview results

Future development will focus on exposing additional workflow capabilities through the API, improving automated testing, adding security controls, and expanding the multi-agent recruitment workflow.
