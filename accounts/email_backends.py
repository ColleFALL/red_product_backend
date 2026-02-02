import os
import requests
from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend


class BrevoAPIEmailBackend(BaseEmailBackend):
    """
    Backend email via Brevo API (HTTPS) - idéal quand SMTP est bloqué (Render).
    Compatible avec Django/Djoser via send_messages().
    """
    API_URL = "https://api.brevo.com/v3/smtp/email"

    def __init__(self, fail_silently=False, **kwargs):
        super().__init__(fail_silently=fail_silently)

        self.api_key = os.environ.get("BREVO_API_KEY", "").strip()
        self.timeout = int(os.environ.get("BREVO_TIMEOUT", "20"))

        # On prend DEFAULT_FROM_EMAIL depuis settings/env, mais on veut un email simple.
        self.from_email = (getattr(settings, "DEFAULT_FROM_EMAIL", "") or os.environ.get("DEFAULT_FROM_EMAIL", "")).strip()

        if not self.api_key and not self.fail_silently:
            raise ValueError("BREVO_API_KEY manquant (Render env).")
        if not self.from_email and not self.fail_silently:
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
            payload = self._build_payload(message)
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

    def _build_payload(self, message):
        to_list = [{"email": e} for e in (message.to or [])]
        cc_list = [{"email": e} for e in (message.cc or [])]
        bcc_list = [{"email": e} for e in (message.bcc or [])]

        text_content = (message.body or "").strip()
        html_content = None

        for alt, mimetype in (getattr(message, "alternatives", None) or []):
            if mimetype == "text/html":
                html_content = alt

        sender_email = self._extract_email(self.from_email)
        if not sender_email:
            raise Exception("Brevo: DEFAULT_FROM_EMAIL invalide (doit être un email simple).")

        data = {
            "sender": {"email": sender_email, "name": "RED PRODUCT"},
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
        """
        Accepte:
        - 'email@domain.com'
        - 'Name <email@domain.com>'
        Retourne toujours 'email@domain.com'
        """
        s = (from_str or "").strip()
        if "<" in s and ">" in s:
            return s.split("<", 1)[1].split(">", 1)[0].strip()
        return s
