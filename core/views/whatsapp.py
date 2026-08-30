"""
Twilio WhatsApp webhook.

Twilio sends incoming WhatsApp messages to this endpoint.

Replies are sent using the Twilio REST API.

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

from core.services.whatsapp import WhatsAppService


logger = logging.getLogger(__name__)


def send_whatsapp_reply(
    to_number: str,
    text: str,
) -> None:

    try:
        WhatsAppService.send(
            to_number,
            text,
        )

    except Exception:
        logger.exception(
            "Failed to send WhatsApp reply"
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

        try:
            WhatsAppService.send(
                to_number,
                (
                    "⚠️ Sorry, the screening job "
                    "failed. Please try again."
                ),
            )

        except Exception:
            logger.exception(
                "Failed to send WhatsApp "
                "background error message"
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

        if not from_number:
            logger.warning(
                "Twilio webhook received "
                "a message without From."
            )

            return HttpResponse(
                status=200
            )

        if not WhatsAppService.can_send():
            logger.error(
                "Twilio credentials are not configured."
            )

            return HttpResponse(
                status=200
            )

        if WhatsAppService.is_slow(parsed):

            threading.Thread(
                target=run_pipeline_in_background,
                args=(
                    from_number,
                    parsed,
                ),
                daemon=True,
            ).start()

            send_whatsapp_reply(
                from_number,
                (
                    "⏳ Screening started. "
                    "I'll send the report and "
                    "interview questions here "
                    "in a moment."
                ),
            )

            return HttpResponse(
                status=200
            )

        reply_text = WhatsAppService.handle(
            parsed
        )

        send_whatsapp_reply(
            from_number,
            reply_text,
        )

        return HttpResponse(
            status=200
        )