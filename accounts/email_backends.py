import os
import requests
from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend


class BrevoAPIEmailBackend(BaseEmailBackend):
    """
    Envoi d'emails via Brevo API (HTTPS) — parfait pour Render où SMTP est bloqué.
    Compatible Django/Djoser via send_messages().
    """
    API_URL = "https://api.brevo.com/v3/smtp/email"

    def __init__(self, fail_silently=False, **kwargs):
        super().__init__(fail_silently=fail_silently)
        self.api_key = os.environ.get("BREVO_API_KEY", "")
        self.timeout = int(os.environ.get("BREVO_TIMEOUT", "20"))

        self.from_raw = getattr(settings, "DEFAULT_FROM_EMAIL", "") or os.environ.get("DEFAULT_FROM_EMAIL", "")

        if not self.api_key and not self.fail_silently:
            raise ValueError("BREVO_API_KEY manquant (Render env).")
        if not self.from_raw and not self.fail_silently:
            raise ValueError("DEFAULT_FROM_EMAIL manquant (settings/env).")

    def send_messages(self, email_messages):
        if not email_messages:
            return 0

        headers = {
            "accept": "application/json",
            "api-key": self.api_key,
            "content-type": "application/json",
        }

        sent = 0
        for message in email_messages:
            payload = self._payload_from_message(message)
            try:
                r = requests.post(self.API_URL, headers=headers, json=payload, timeout=self.timeout)
                if r.status_code >= 400:
                    raise Exception(f"Brevo API error {r.status_code}: {r.text}")
                sent += 1
            except Exception:
                if self.fail_silently:
                    continue
                raise

        return sent

    def _payload_from_message(self, message):
        to_list = [{"email": e} for e in (message.to or [])]
        cc_list = [{"email": e} for e in (message.cc or [])]
        bcc_list = [{"email": e} for e in (message.bcc or [])]

        text_content = (message.body or "").strip()
        html_content = None

        for alt, mimetype in getattr(message, "alternatives", []) or []:
            if mimetype == "text/html":
                html_content = alt

        sender_email = self._extract_email(self.from_raw)
        sender_name = self._extract_name(self.from_raw) or "RED PRODUCT"

        data = {
            "sender": {"email": sender_email, "name": sender_name},
            "to": to_list,
            "subject": message.subject or "",
        }
        if cc_list:
            data["cc"] = cc_list
        if bcc_list:
            data["bcc"] = bcc_list

        if html_content:
            data["htmlContent"] = html_content
            if text_content:
                data["textContent"] = text_content
        else:
            data["textContent"] = text_content or " "

        return data

    @staticmethod
    def _extract_email(from_str: str) -> str:
        if "<" in from_str and ">" in from_str:
            return from_str.split("<", 1)[1].split(">", 1)[0].strip()
        return from_str.strip()

    @staticmethod
    def _extract_name(from_str: str) -> str:
        if "<" in from_str:
            return from_str.split("<", 1)[0].strip().strip('"')
        return ""
