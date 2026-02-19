from django.dispatch import receiver
from djoser.signals import user_registered
from django.utils.http import urlquote

@receiver(user_registered)
def encode_activation_token(sender, user, request, **kwargs):
    # On encode le token qui sera envoyé par email
    if hasattr(user, 'activation_token'):
        user.activation_token = urlquote(user.activation_token)
