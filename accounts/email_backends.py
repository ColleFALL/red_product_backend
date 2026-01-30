import os
import requests
from django.core.mail.backends.base import BaseEmailBackend

BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"

class BrevoAPIEmailBackend(BaseEmailBackend):
    """
    Envoi d'emails via Brevo Transactional Email API (HTTP).
    Fonctionne sur Render même si SMTP est bloqué.
    """

    def send_messages(self, email_messages):
        api_key = os.environ.get("BREVO_API_KEY")
        if not api_key:
            raise ValueError("BREVO_API_KEY manquant dans les variables d'environnement")

        headers = {
            "accept": "application/json",
            "api-key": api_key,
            "content-type": "application/json",
        }

        default_from = os.environ.get("DEFAULT_FROM_EMAIL", "")
        sent = 0

        for msg in email_messages:
            from_email = msg.from_email or default_from
            if not from_email:
                raise ValueError("DEFAULT_FROM_EMAIL manquant (ou msg.from_email vide)")

            to_emails = msg.to or []
            if not to_emails:
                continue

            # Support "Nom <email@domaine>"
            if "<" in from_email and ">" in from_email:
                name = from_email.split("<")[0].strip()
                email = from_email.split("<")[1].replace(">", "").strip()
            else:
                name = "RED PRODUCT"
                email = from_email.strip()

            payload = {
                "sender": {"name": name or "RED PRODUCT", "email": email},
                "to": [{"email": e} for e in to_emails],
                "subject": msg.subject or "",
                "htmlContent": msg.body or "",
            }

            r = requests.post(BREVO_API_URL, json=payload, headers=headers, timeout=20)

            if 200 <= r.status_code < 300:
                sent += 1
            else:
                if not self.fail_silently:
                    raise Exception(f"Brevo API error {r.status_code}: {r.text}")

        return sent
