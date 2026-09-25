import logging
from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

logger = logging.getLogger(__name__)
User = get_user_model()


@shared_task
def send_welcome_email_task(user_id):
    """Envoie un e-mail de bienvenue asynchrone lors de l'inscription."""
    try:
        user = User.objects.get(pk=user_id)
        subject = "Bienvenue sur INVENTO !"
        message = (
            f"Bonjour {user.first_name},\n\n"
            f"Toute l'équipe INVENTO est ravie de vous accueillir.\n"
            f"Vous pouvez maintenant compléter votre profil, ajouter vos projets et publier votre portfolio.\n\n"
            f"L'équipe INVENTO."
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@invento.com'),
            recipient_list=[user.email],
            fail_silently=True
        )
        logger.info(f"E-mail de bienvenue envoyé à {user.email}")
    except User.DoesNotExist:
        logger.error(f"Utilisateur {user_id} non trouvé pour l'envoi d'e-mail.")


@shared_task
def clean_expired_blacklisted_tokens():
    """Nettoie les jetons JWT révoqués qui ont expiré."""
    now = timezone.now()
    deleted_count, _ = OutstandingToken.objects.filter(expires_at__lt=now).delete()
    logger.info(f"Nettoyage Celery : {deleted_count} jetons expirés supprimés.")
    return deleted_count
