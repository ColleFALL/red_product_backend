import google.generativeai as genai
from django.conf import settings

# Configuration de Gemini avec la clé API
genai.configure(api_key=settings.GEMINI_API_KEY)


def ask_gemini(message, context_data, history=None):
    """
    Envoie une requête à Gemini avec le contexte Red Product.
    
    Args:
        message: Question de l'admin
        context_data: Données en temps réel (hotels, stats, etc.)
        history: Historique de la conversation
    
    Returns:
        str: Réponse de Gemini
    """
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")

        system_prompt = """
Tu es l'assistant officiel de Red Product.
Tu aides l'administrateur à gérer ses hôtels.
Tu as accès aux données en temps réel.
Sois professionnel, précis et concis.
Réponds toujours en français.
        """

        # Formater l'historique de manière lisible
        history_text = ""
        if history:
            for msg in history:
                role = "Admin" if msg["role"] == "user" else "Assistant"
                history_text += f"{role}: {msg['content']}\n"

        full_prompt = f"""
{system_prompt}

Données actuelles :
{context_data}

Historique de conversation :
{history_text if history_text else "Aucun historique"}

Question admin :
{message}
"""

        response = model.generate_content(full_prompt)
        
        return response.text

    except Exception as e:
        # En cas d'erreur Gemini, retourner un message clair
        return f"Désolé, je rencontre une erreur technique : {str(e)}"