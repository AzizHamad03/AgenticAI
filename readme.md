# Agentic AI Recruitment System

An AI-powered recruitment backend built with **Django**, **Django REST Framework**, **PostgreSQL**, **CrewAI**, and **OpenAI**.

The goal of this project is to build an intelligent recruitment platform that uses specialized AI agents to assist with tasks such as resume screening, candidate evaluation, job matching, and interview question generation.

> **Project Status:** 🚧 Early Development  
> This project is under active development. The current version provides the core recruitment data models and initial REST API layer. AI agents, automated workflows, testing, authentication, and additional features will be added as the project evolves.

---

## Overview

The Agentic AI Recruitment System is designed to automate and assist with different stages of the recruitment process.

The planned workflow includes:

1. Creating departments and job positions.
2. Registering candidates.
3. Uploading candidate resumes.
4. Screening resumes against job requirements.
5. Generating structured candidate evaluations.
6. Generating personalized interview questions.
7. Coordinating recruitment tasks through specialized AI agents.

The project follows a modular architecture so that new services, APIs, and AI agents can be added without tightly coupling the different parts of the system.

---

## Current Features

The current implementation includes:

- Department management
- Job position management
- Candidate registration
- Resume uploads
- Resume file-type validation
- Resume screening result storage
- Interview question set storage
- PostgreSQL database integration
- Django REST Framework serializers
- Custom DRF `APIView` endpoints
- Structured API validation and error handling
- Environment-based configuration
- Django Admin integration
- OpenAI configuration
- CrewAI dependencies for future agent development

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

## Example Requests

### Create a Job Position

```http
POST /api/job-positions/
```

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

The response can include:

- Candidate
- Job position
- Match score
- Strengths
- Missing skills
- Recommendation
- Summary
- Raw report
- Generation timestamp

---

### Retrieve Interview Questions

```http
GET /api/interview-question-sets/1/
```

The response contains:

- Technical questions
- Behavioral questions
- Follow-up questions
- Candidate
- Job position
- Screening result
- Generation timestamp

---

## AI Agent Architecture

The project is being designed around multiple specialized AI agents.

### Resume Screening Agent

The Resume Screening Agent will evaluate a candidate's resume against the requirements of a job position.

Screening results are designed to include:

- Match score
- Candidate strengths
- Missing skills
- Recommendation
  - Proceed to interview
  - Hold for review
  - Reject
- Screening summary
- Raw AI-generated report

### Interview Question Generator

The Interview Question Generator will use information from the:

- Candidate
- Job position
- Screening result

to generate personalized:

- Technical questions
- Behavioral questions
- Follow-up questions

### Future Agents

Additional agents may be introduced for tasks such as:

- Candidate ranking
- Skill-gap analysis
- Candidate-to-job matching
- Interview evaluation
- Recruitment recommendations
- Workflow coordination

---

## Tech Stack

### Backend

- Python
- Django 4.2
- Django REST Framework

### Database

- PostgreSQL

### AI

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
│   ├── admin.py
│   ├── apps.py
│   └── urls.py
│
├── media/
│   └── resumes/
│
├── .env.example
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md
```

The structure will continue to expand as AI agents, services, tests, authentication, and additional APIs are introduced.

---

## Data Models

### Department

Represents a department within the organization.

### JobPosition

Represents an available position and stores information such as:

- Job title
- Department
- Description
- Required skills

### Candidate

Stores candidate information including:

- Full name
- Email
- Phone number
- Creation date

### Resume

Associates an uploaded resume file with a candidate.

### ScreeningResult

Stores the structured result of evaluating a candidate against a job position.

The model supports information such as:

- Match score
- Strengths
- Missing skills
- Recommendation
- Summary
- Raw screening report

### InterviewQuestionSet

Stores interview questions associated with a candidate, job position, and screening result.

Question categories include:

- Technical questions
- Behavioral questions
- Follow-up questions

---

## Getting Started

### 1. Clone the Repository

```bash
git clone <repository-url>
cd AgenticAI
```

### 2. Create a Virtual Environment

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

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

> Never commit your real `.env` file, database credentials, or API keys to version control.

---

## Database Setup

Make sure PostgreSQL is installed and running.

Create the PostgreSQL database specified in your `.env` file, then apply the Django migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Run the Development Server

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

## Create an Admin User

Create a Django superuser with:

```bash
python manage.py createsuperuser
```

Then start the server and visit:

```text
http://127.0.0.1:8000/admin/
```

The Django Admin interface can currently be used to manage departments, job positions, candidates, resumes, screening results, and interview question sets.

---

## Development Checks

Run Django's built-in system checks with:

```bash
python manage.py check
```

A correctly configured project should return:

```text
System check identified no issues (0 silenced).
```

---

## Roadmap

The project is still in its early stages.

### Completed

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

### Planned

- [ ] Resume text extraction
- [ ] Resume Screening AI Agent
- [ ] Interview Question Generation Agent
- [ ] CrewAI agent orchestration
- [ ] Structured AI output validation
- [ ] Candidate/job matching workflow
- [ ] Candidate ranking
- [ ] Authentication and authorization
- [ ] API documentation
- [ ] Automated unit and API tests
- [ ] Logging and monitoring
- [ ] Frontend integration
- [ ] Deployment configuration

The roadmap will continue to evolve as development progresses.

---

## Future Vision

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

## Security

Sensitive information such as:

- OpenAI API keys
- Database passwords
- Django secret keys

should always be stored in environment variables.

The `.env` file should remain excluded from version control through `.gitignore`.

Additional authentication, authorization, and production security measures will be introduced as the project develops.

---

## Contributing

The project is currently under active development.

Contribution guidelines, coding conventions, testing requirements, and development workflows may be introduced as the codebase matures.

---

## License

A license has not yet been selected for this project.

---

## Development Status

**Current Stage:** Early Development — Core Backend & Initial REST API

The project currently provides the foundational recruitment data layer and REST API functionality.

The next major development phase will focus on implementing the AI agent layer, including resume analysis, candidate evaluation, and interview question generation.

Features, architecture, and APIs may continue to change as the project develops.