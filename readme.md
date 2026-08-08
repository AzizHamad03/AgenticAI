# Agentic AI Recruitment System

An AI-powered recruitment backend built with **Django**, **Django REST Framework**, **PostgreSQL**, **CrewAI**, and **OpenAI**.

The goal of this project is to build an intelligent recruitment system that uses AI agents to assist with tasks such as resume screening, candidate evaluation, and interview question generation.

> **Project Status:** 🚧 Early Development
> This project is currently under active development. The existing implementation represents the initial backend structure, and more features, APIs, AI agents, testing, and documentation will be added over time.

---

## Overview

The Agentic AI Recruitment System is designed to help automate parts of the hiring process using specialized AI agents.

The planned workflow includes:

1. Creating departments and job positions.
2. Registering candidates.
3. Uploading candidate resumes.
4. Screening resumes against job requirements.
5. Generating structured candidate evaluations.
6. Generating personalized interview questions.
7. Expanding the system with additional AI-powered recruitment workflows.

The project uses a modular architecture so that new agents and recruitment features can be added as development continues.

---

## Current Features

The current version includes the initial backend foundation for:

* Department management
* Job position management
* Candidate management
* Resume storage
* Resume screening results
* Interview question sets
* PostgreSQL database integration
* Django REST Framework serializers
* Environment-based configuration
* OpenAI configuration
* Initial CrewAI dependencies for AI agent development

---

## AI Agent Architecture

The project is being designed around multiple specialized AI agents.

### Resume Screening Agent

The Resume Screening Agent will analyze a candidate's resume against a job position.

Screening results are designed to include:

* Match score
* Candidate strengths
* Missing skills
* Recommendation

  * Proceed to interview
  * Hold for review
  * Reject
* Screening summary
* Raw AI-generated report

### Interview Question Generator

The Interview Question Generator will use information about the:

* Candidate
* Job position
* Resume screening result

to generate customized:

* Technical questions
* Behavioral questions
* Follow-up questions

Additional AI agents may be introduced as the project evolves.

---

## Tech Stack

### Backend

* Python
* Django 4.2
* Django REST Framework

### Database

* PostgreSQL

### AI

* CrewAI
* OpenAI API
* CrewAI Tools

### Document Processing

* PDFPlumber
* python-docx

### Configuration

* python-decouple

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
│   │   └── __init__.py
│   │
│   ├── admin.py
│   └── apps.py
│
├── .env.example
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md
```

The structure will expand as API endpoints, AI agents, services, tests, and other components are implemented.

---

## Data Models

The current system contains the following core models.

### Department

Represents a department within the organization.

### JobPosition

Represents an available job position and contains information such as:

* Job title
* Department
* Description
* Required skills

### Candidate

Stores basic candidate information including:

* Full name
* Email
* Phone number
* Creation date

### Resume

Stores uploaded candidate resumes and associates them with candidates.

### ScreeningResult

Stores the structured output generated when a candidate is evaluated against a job position.

### InterviewQuestionSet

Stores AI-generated interview questions associated with a candidate and job position.

---

## Getting Started

### 1. Clone the repository

```bash
git clone <repository-url>
cd AgenticAI
```

---

### 2. Create a virtual environment

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

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root.

You can use `.env.example` as a template:

```bash
cp .env.example .env
```

Configure the following values:

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

Never commit your real `.env` file or API keys to GitHub.

---

## Database Setup

Make sure PostgreSQL is installed and running.

Create the database specified in your `.env` file and then run:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Run the Development Server

Start Django with:

```bash
python manage.py runserver
```

The development server will normally be available at:

```text
http://127.0.0.1:8000/
```

The Django admin interface is available at:

```text
http://127.0.0.1:8000/admin/
```

---

## Create an Admin User

To access Django Admin:

```bash
python manage.py createsuperuser
```

Then start the server and visit:

```text
http://127.0.0.1:8000/admin/
```

---

## Roadmap

This project is still in its early stages. Planned development includes:

* [x] Initial Django project setup
* [x] PostgreSQL configuration
* [x] Core recruitment models
* [x] Initial DRF serializers
* [x] Resume screening result model
* [x] Interview question set model
* [ ] Complete REST API endpoints
* [ ] Resume upload API
* [ ] Resume text extraction
* [ ] Resume Screening AI Agent
* [ ] Interview Question Generation Agent
* [ ] CrewAI orchestration
* [ ] Structured AI output validation
* [ ] Candidate/job matching workflow
* [ ] API error handling
* [ ] Authentication and authorization
* [ ] API documentation
* [ ] Automated tests
* [ ] Logging and monitoring
* [ ] Frontend integration
* [ ] Deployment configuration

The roadmap will continue to evolve as the project grows.

---

## Future Vision

The long-term goal is to develop the project into a multi-agent recruitment platform where specialized AI agents collaborate throughout the hiring process.

Possible future capabilities include:

* Intelligent resume analysis
* Candidate ranking
* Skill-gap detection
* Job-to-candidate matching
* Personalized interview generation
* Interview evaluation
* Candidate summaries
* Recruitment recommendations
* Automated recruitment workflows
* Human review and approval steps
* Recruitment analytics

The focus is not simply to use an LLM, but to create structured and maintainable **agentic workflows** that can support real recruitment processes.

---

## Security

Sensitive information such as:

* OpenAI API keys
* Database passwords
* Django secret keys

should always be stored in environment variables.

The `.env` file is excluded from version control using `.gitignore`.

---

## Contributing

The project is currently in active development.

As the codebase becomes more mature, contribution guidelines and development conventions may be added.

---

## License

A license has not yet been selected for this project.

---

## Development Status

**Version:** Early Development / Initial Backend Setup

This repository currently represents the foundation of the project rather than a finished product. Features, architecture, documentation, and APIs are expected to change significantly as development continues.
