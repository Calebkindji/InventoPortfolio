from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel
from apps.core.validators import FileSizeValidator, validate_image_extension


class UserProfile(TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    profile_picture = models.ImageField(
        upload_to='profiles/pictures/',
        null=True,
        blank=True,
        validators=[FileSizeValidator(5), validate_image_extension],
        verbose_name="Photo de profil"
    )
    title = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Titre professionnel"
    )
    bio = models.TextField(
        blank=True,
        verbose_name="Biographie"
    )
    location = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Localisation générale"
    )
    professional_email = models.EmailField(
        blank=True,
        verbose_name="Adresse e-mail professionnelle"
    )
    phone_number = models.CharField(
        max_length=30,
        blank=True,
        verbose_name="Numéro professionnel"
    )
    website_url = models.URLField(blank=True, verbose_name="Site personnel")
    github_url = models.URLField(blank=True, verbose_name="Lien GitHub")
    gitlab_url = models.URLField(blank=True, verbose_name="Lien GitLab")
    linkedin_url = models.URLField(blank=True, verbose_name="Lien LinkedIn")
    other_links = models.JSONField(
        default=list,
        blank=True,
        help_text="Liste de liens professionnels personnalisés, ex: [{'title': 'Behance', 'url': '...'}]"
    )

    def __str__(self):
        return f"Profil de {self.user.get_full_name()}"
