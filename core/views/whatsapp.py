"""
Twilio WhatsApp webhook.

Twilio sends incoming WhatsApp messages to this endpoint.
Fast commands reply immediately.

The slower "run" command is processed in a background
thread so the webhook can respond quickly.
"""

import logging
import threading

from django.db import close_old_connections
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from core.services.whatsapp import (
    WhatsAppService,
    split_message,
)


logger = logging.getLogger(__name__)


def build_twiml_reply(
    text: str,
) -> HttpResponse:

    from twilio.twiml.messaging_response import (
        MessagingResponse,
    )

    response = MessagingResponse()

    for piece in split_message(text):
        response.message(piece)

    return HttpResponse(
        str(response),
        content_type="application/xml",
    )


def run_pipeline_in_background(
    to_number: str,
    parsed,
) -> None:

    close_old_connections()

    try:

        reply_text = WhatsAppService.handle(
            parsed
        )

        WhatsAppService.send(
            to_number,
            reply_text,
        )

    except Exception:

        logger.exception(
            "Background WhatsApp job failed"
        )

        WhatsAppService.send(
            to_number,
            (
                "⚠️ Sorry, the screening job "
                "failed. Please try again."
            ),
        )

    finally:
        close_old_connections()


@method_decorator(
    csrf_exempt,
    name="dispatch",
)
class TwilioWhatsAppWebhookView(View):

    def get(
        self,
        request,
        *args,
        **kwargs,
    ):

        return HttpResponse(
            "WhatsApp webhook is live. "
            "Set this URL in Twilio."
        )

    def post(
        self,
        request,
        *args,
        **kwargs,
    ):

        message_text = request.POST.get(
            "Body",
            "",
        )

        from_number = request.POST.get(
            "From",
            "",
        )

        parsed = WhatsAppService.parse(
            message_text
        )

        can_reply_later = (
            WhatsAppService.can_send()
            and from_number
        )

        if (
            WhatsAppService.is_slow(parsed)
            and can_reply_later
        ):

            threading.Thread(
                target=run_pipeline_in_background,
                args=(
                    from_number,
                    parsed,
                ),
                daemon=True,
            ).start()

            return build_twiml_reply(
                "⏳ Screening started. "
                "I'll send the report and "
                "interview questions here "
                "in a moment."
            )

        reply_text = (
            WhatsAppService.handle(parsed)
        )

        return build_twiml_reply(
            reply_text
        )