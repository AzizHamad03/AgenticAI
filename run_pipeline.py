import json
import os

import django
from docx import Document
from pypdf import PdfReader


def setup_django():
    """
    Initialize Django before importing project modules that may depend
    on Django settings or models.
    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    django.setup()


def extract_resume_text(file_path: str) -> str:
    """
    Extract resume text from PDF, DOCX, or TXT files.
    """
    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        reader = PdfReader(file_path)

        pages_text = []

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                pages_text.append(page_text)

        return "\n".join(pages_text)

    if extension == ".docx":
        document = Document(file_path)

        return "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        )

    if extension == ".txt":
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    raise ValueError(
        "Unsupported resume format. Please use PDF, DOCX, or TXT."
    )


def main():
    # --------------------------------------------------
    # INITIALIZE DJANGO
    # --------------------------------------------------

    setup_django()

    # Import after Django is initialized
    from core.flows.hr_pipeline.flow import HRPipelineFlow

    # --------------------------------------------------
    # TEST INPUTS
    # --------------------------------------------------

    resume_path = "media/resumes/Abedalaziz_Hamad_CV.pdf"

    job_title = "Backend Engineer"

    job_description = """
    We are looking for a Backend Engineer to build and maintain
    scalable backend applications and REST APIs.

    The ideal candidate should have experience with Python,
    Django, PostgreSQL, API development, and software engineering
    best practices.

    The candidate should be able to collaborate with other
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
            f"Resume file was not found: {resume_path}"
        )

    resume_text = extract_resume_text(resume_path)

    if not resume_text.strip():
        raise ValueError(
            f"No text could be extracted from resume: {resume_path}"
        )

    print("Resume loaded successfully.")

    # --------------------------------------------------
    # CREATE HR PIPELINE FLOW
    # --------------------------------------------------

    print("Starting HR pipeline...")

    flow = HRPipelineFlow()

    # --------------------------------------------------
    # SET INITIAL FLOW STATE
    # --------------------------------------------------

    flow.state.candidate_resume = resume_text
    flow.state.job_title = job_title
    flow.state.job_description = job_description
    flow.state.required_skills = required_skills

    # --------------------------------------------------
    # RUN PIPELINE
    # --------------------------------------------------

    result = flow.kickoff()

    # --------------------------------------------------
    # PRINT FINAL RESULT
    # --------------------------------------------------

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