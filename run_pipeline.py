import json
import os

import django


def setup_django():
    """
    Initialize Django before importing project modules
    that depend on Django.
    """

    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "config.settings",
    )

    django.setup()


def main():

    # --------------------------------------------------
    # INITIALIZE DJANGO
    # --------------------------------------------------

    setup_django()

    # Import after Django setup.
    from core.flows.hr_pipeline.flow import (
        HRPipelineFlow,
    )

    from core.services.resume_parser import (
        extract_resume_text,
    )

    # --------------------------------------------------
    # RAW DEMO INPUTS
    # --------------------------------------------------

    resume_path = (
        "media/resumes/Abedalaziz_Hamad_CV.pdf"
    )

    job_title = "Backend Engineer"

    job_description = """
    We are looking for a Backend Engineer to build and maintain
    scalable backend applications and REST APIs.

    The engineer should have experience with Python, Django,
    PostgreSQL, REST APIs, Git, and backend development.

    The candidate should collaborate effectively with other
    developers, debug technical issues, and write clean,
    maintainable code.
    """

    required_skills = [
        "Python",
        "Django",
        "PostgreSQL",
        "REST APIs",
        "Git",
    ]

    # --------------------------------------------------
    # READ RESUME
    # --------------------------------------------------

    print("Reading resume...")

    if not os.path.exists(resume_path):

        raise FileNotFoundError(
            f"Resume file was not found: "
            f"{resume_path}"
        )

    resume_text = extract_resume_text(
        resume_path
    )

    if not resume_text:

        raise ValueError(
            "No text could be extracted from "
            f"resume: {resume_path}"
        )

    print("Resume loaded successfully.")

    # --------------------------------------------------
    # RUN RAW MODE
    # --------------------------------------------------

    print("Starting HR pipeline...")

    flow = HRPipelineFlow()

    result = flow.kickoff(
        candidate_resume=resume_text,
        job_title=job_title,
        job_description=job_description,
        required_skills=required_skills,
    )

    print("\nHR pipeline completed.\n")

    print(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False,
            default=str,
        )
    )


if __name__ == "__main__":
    main()