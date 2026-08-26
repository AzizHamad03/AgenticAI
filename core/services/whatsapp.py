"""
WhatsApp business logic.

This service parses WhatsApp commands, calls the existing
HR pipeline, and formats the results for WhatsApp.
"""

import logging
from dataclasses import dataclass
from typing import Optional

from django.conf import settings

from core.services.pipeline_service import (
    PipelineService,
    ResolutionError,
)


logger = logging.getLogger(__name__)


MAX_WHATSAPP_CHARS = 1500


HELP_TEXT = (
    "AI-HRMS bot\n\n"
    "Send one of these:\n"
    "  run <candidate> ; <job> -> screen + interview questions\n"
    "  get <candidate> ; <job> -> fetch latest stored results\n\n"
    "Candidate and job can be an id or a name.\n"
    "Examples:\n"
    "  run Jane Doe ; Backend Engineer\n"
    "  get 1 ; 2"
)


@dataclass
class ParsedCommand:
    action: Optional[str] = None
    candidate_ref: str = ""
    job_ref: str = ""
    error: str = ""


def split_message(
    text: str,
    limit: int = MAX_WHATSAPP_CHARS,
) -> list[str]:
    return [
        text[i:i + limit]
        for i in range(0, len(text), limit)
    ]


class WhatsAppService:

    @staticmethod
    def parse(body: str) -> ParsedCommand:

        text = (body or "").strip()

        if not text or text.lower() == "help":
            return ParsedCommand(
                action="help"
            )

        first_word, _, rest = text.partition(" ")

        if first_word.lower() in (
            "run",
            "get",
        ):
            action = first_word.lower()
            text = rest.strip()

        else:
            action = None

        if ";" not in text:
            return ParsedCommand(
                action=None,
                error=(
                    "Please separate the candidate and job "
                    "with ';'.\n"
                    "Example: run Jane Doe ; Backend Engineer"
                ),
            )

        candidate_ref, _, job_ref = text.partition(";")

        candidate_ref = candidate_ref.strip()
        job_ref = job_ref.strip()

        if not candidate_ref or not job_ref:
            return ParsedCommand(
                action=None,
                error=(
                    "I need BOTH a candidate and a job.\n"
                    "Example: run 1 ; 2"
                ),
            )

        if action is None:

            both_are_ids = (
                candidate_ref.isdigit()
                and job_ref.isdigit()
            )

            action = (
                "get"
                if both_are_ids
                else "run"
            )

        return ParsedCommand(
            action=action,
            candidate_ref=candidate_ref,
            job_ref=job_ref,
        )

    @staticmethod
    def handle(
        parsed: ParsedCommand,
    ) -> str:

        if parsed.action == "help":
            return HELP_TEXT

        if parsed.error:
            return (
                "⚠️ "
                + parsed.error
                + "\n\nSend 'help' for usage."
            )

        try:
            candidate = (
                PipelineService.resolve_candidate(
                    parsed.candidate_ref
                )
            )

            job = PipelineService.resolve_job(
                parsed.job_ref
            )

        except ResolutionError as exc:
            return "⚠️ " + str(exc)

        try:

            if parsed.action == "get":

                screening, questions = (
                    PipelineService.latest(
                        candidate,
                        job,
                    )
                )

                if screening is None:
                    return (
                        "No screening found yet for "
                        f"{candidate.full_name} / "
                        f"{job.title}.\n"
                        "Send: "
                        f"run {candidate.id} ; {job.id}"
                    )

            else:

                screening, questions = (
                    PipelineService.run(
                        candidate,
                        job,
                    )
                )

        except Exception as exc:
            logger.exception(
                "WhatsApp pipeline failed"
            )

            return (
                "⚠️ Something went wrong: "
                f"{exc}"
            )

        return WhatsAppService.format_results(
            candidate,
            job,
            screening,
            questions,
        )

    @staticmethod
    def format_results(
        candidate,
        job,
        screening,
        questions,
    ) -> str:

        text = _format_screening(
            candidate,
            job,
            screening,
        )

        if questions is not None:
            text += (
                "\n\n"
                + _format_questions(
                    candidate,
                    job,
                    questions,
                )
            )

        return text

    @staticmethod
    def is_slow(
        parsed: ParsedCommand,
    ) -> bool:

        return parsed.action == "run"

    @staticmethod
    def can_send() -> bool:

        return bool(
            settings.TWILIO_ACCOUNT_SID
            and settings.TWILIO_AUTH_TOKEN
            and settings.TWILIO_WHATSAPP_FROM
        )

    @staticmethod
    def send(
        to: str,
        text: str,
    ) -> None:

        from twilio.rest import Client

        client = Client(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN,
        )

        for piece in split_message(text):

            client.messages.create(
                from_=settings.TWILIO_WHATSAPP_FROM,
                to=to,
                body=piece,
            )


def _format_screening(
    candidate,
    job,
    screening,
) -> str:

    strengths = (
        ", ".join(screening.strengths)
        if screening.strengths
        else "—"
    )

    missing = (
        ", ".join(screening.missing_skills)
        if screening.missing_skills
        else "—"
    )

    score = screening.score

    if float(score).is_integer():
        score = int(score)

    return (
        f"*Screening* — "
        f"{candidate.full_name} / {job.title}\n"
        f"Score: {score}/100\n"
        "Recommendation: "
        f"{screening.get_recommendation_display()}\n"
        f"Strengths: {strengths}\n"
        f"Missing skills: {missing}\n"
        f"Summary: {screening.summary or '—'}"
    )


def _format_questions(
    candidate,
    job,
    questions,
) -> str:

    def block(
        title,
        items,
    ):

        if not items:
            return f"{title}:\n  —"

        lines = "\n".join(
            f"  {number}. {question}"
            for number, question
            in enumerate(
                items,
                start=1,
            )
        )

        return (
            f"{title}:\n"
            f"{lines}"
        )

    return (
        f"*Interview questions* — "
        f"{candidate.full_name} / {job.title}\n"
        + block(
            "Technical",
            questions.technical_questions,
        )
        + "\n"
        + block(
            "Behavioral",
            questions.behavioral_questions,
        )
        + "\n"
        + block(
            "Follow-up",
            questions.follow_up_questions,
        )
    )