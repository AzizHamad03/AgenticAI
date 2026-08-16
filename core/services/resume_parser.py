"""Utilities for extracting plain text from uploaded resume files."""

from contextlib import contextmanager
from pathlib import Path
from typing import BinaryIO, Iterator, Union

import pdfplumber
from docx import Document


ResumeSource = Union[str, Path, object]


@contextmanager
def _open_resume(source: ResumeSource) -> Iterator[BinaryIO]:
    """
    Open either:

    - a normal filesystem path
    - a Django FieldFile

    as binary data.
    """

    # Raw demo mode:
    # source will normally be something like:
    # "media/resumes/my_resume.pdf"
    if isinstance(source, (str, Path)):
        with open(source, "rb") as file_obj:
            yield file_obj
        return

    # Database mode:
    # source will be a Django FieldFile from Resume.file.
    source.open("rb")

    try:
        yield source
    finally:
        source.close()


def extract_resume_text(source: ResumeSource) -> str:
    """
    Extract text from a PDF, DOCX, or TXT resume.

    The source can be either:

    - a filesystem path
    - a Django FieldFile
    """

    name = getattr(source, "name", str(source))

    extension = Path(name).suffix.lower()

    with _open_resume(source) as file_obj:

        if extension == ".pdf":
            with pdfplumber.open(file_obj) as pdf:

                text = "\n".join(
                    page_text
                    for page in pdf.pages
                    if (page_text := page.extract_text())
                )

        elif extension == ".docx":

            document = Document(file_obj)

            text = "\n".join(
                paragraph.text
                for paragraph in document.paragraphs
                if paragraph.text.strip()
            )

        elif extension == ".txt":

            raw = file_obj.read()

            text = (
                raw.decode("utf-8")
                if isinstance(raw, bytes)
                else raw
            )

        else:
            raise ValueError(
                "Unsupported resume format. "
                "Please use PDF, DOCX, or TXT."
            )

    return text.strip()